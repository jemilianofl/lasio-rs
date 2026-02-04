use crate::{CurveItem, HeaderItem, LASFile};
use std::io::BufRead;
use ndarray::Array2;
use nom::{
    bytes::complete::{tag, take_while, take_while1},
    character::complete::{char, space0},
    combinator::{opt, rest},
    sequence::preceded,
    IResult,
};

#[derive(Debug, PartialEq, Clone)]
enum LineType {
    SectionTitle(String),
    HeaderItem(HeaderItem),
    Comment,
    Empty,
    DataLine(String), 
}

fn is_mnemonic_char(c: char) -> bool {
    !c.is_whitespace() && c != '.' && c != ':'
}

fn parse_mnemonic(input: &str) -> IResult<&str, &str> {
    take_while1(is_mnemonic_char)(input)
}

fn parse_unit(input: &str) -> IResult<&str, &str> {
    take_while(|c: char| !c.is_whitespace() && c != ':') (input)
}

fn parse_line_header(input: &str) -> IResult<&str, HeaderItem> {
    let (input, mnemonic) = parse_mnemonic(input)?;
    let (input, _) = space0(input)?;
    
    let (input, unit) = opt(preceded(char('.'), parse_unit))(input)?;
    let unit = unit.unwrap_or("");
    
    let (input, _) = space0(input)?;
    
    let (input, value_str) = take_while(|c| c != ':')(input)?;
    
    let (_input, descr) = if input.starts_with(':') {
        preceded(char(':'), rest)(input)?
    } else {
        (input, "")
    };
    
    Ok(("", HeaderItem::new(mnemonic, unit, value_str.trim(), descr.trim())))
}


fn parse_section_title(input: &str) -> IResult<&str, String> {
    let (input, _) = tag("~")(input)?;
    let (_input, title) = rest(input)?;
    Ok(("", title.trim().to_string()))
}

fn parse_comment(input: &str) -> IResult<&str, ()> {
    let (input, _) = char('#')(input)?;
    let (_input, _) = rest(input)?;
    Ok(("", ()))
}

fn parse_line(input: &str) -> IResult<&str, LineType> {
    let input = input.trim();
    if input.is_empty() {
        return Ok(("", LineType::Empty));
    }
    
    if input.starts_with('#') {
        let _ = parse_comment(input)?;
        return Ok(("", LineType::Comment));
    }
    
    if input.starts_with('~') {
        let (_, title) = parse_section_title(input)?;
        return Ok(("", LineType::SectionTitle(title)));
    }
    
    match parse_line_header(input) {
        Ok((_, item)) => Ok(("", LineType::HeaderItem(item))),
        Err(_) => {
            Ok(("", LineType::DataLine(input.to_string())))
        }
    }
}

use rayon::prelude::*;

const CHUNK_SIZE: usize = 10000;

pub fn parse_las_from_reader<R: BufRead>(reader: R) -> Result<LASFile, Box<dyn std::error::Error>> {
    let mut las = LASFile::default();
    let mut current_section = "None".to_string();
    let mut data_values: Vec<f64> = Vec::new();
    let mut ncols = 0;
    
    // Chunk buffer for data lines
    let mut line_chunk: Vec<String> = Vec::with_capacity(CHUNK_SIZE);
    
    // Helper closure to process chunk
    let process_chunk = |chunk: &Vec<String>, data_vals: &mut Vec<f64>, ncols_ref: &mut usize| {
        if chunk.is_empty() { return; }
        // Parse in parallel
        let parsed_rows: Vec<Vec<f64>> = chunk.par_iter()
            .map(|line| {
                 line.split_whitespace()
                    .filter_map(|s| s.parse::<f64>().ok())
                    .collect()
            })
            .collect();
        
        for row in parsed_rows {
            if !row.is_empty() {
                if *ncols_ref == 0 {
                    *ncols_ref = row.len();
                }
                data_vals.extend(row);
            }
        }
    };
    
    for line_result in reader.lines() {
        let line = line_result?;
        
        // Optimize for Data section
        if current_section.starts_with('A') || current_section.contains("ASCII") {
             // Check if we hit a new section
             if line.trim().starts_with('~') {
                  // Flus chunk
                  process_chunk(&line_chunk, &mut data_values, &mut ncols);
                  line_chunk.clear();
                  
                  let (_, title) = parse_section_title(line.trim()).unwrap_or(("", "Unknown".to_string()));
                  current_section = title;
                  continue;
             }
             
             line_chunk.push(line);
             
             if line_chunk.len() >= CHUNK_SIZE {
                 process_chunk(&line_chunk, &mut data_values, &mut ncols);
                 line_chunk.clear();
             }
             continue;
        }

        match parse_line(&line) {
            Ok((_, LineType::SectionTitle(title))) => {
                current_section = title;
            },
            Ok((_, LineType::HeaderItem(item))) => {
                let s = current_section.chars().nth(0).unwrap_or(' ').to_ascii_uppercase();
                match s {
                    'V' => las.version.insert(item),
                    'W' => las.well.insert(item),
                    'P' => las.params.insert(item),
                    'C' => {
                         let curve = CurveItem::new(&item.mnemonic, &item.unit, &item.value, &item.descr);
                         las.curves.insert(curve);
                    },
                    _ => {
                        // param/other?
                    }
                }
            },
            Ok((_, LineType::DataLine(content))) => {
                if current_section.starts_with('O') {
                    las.other.push_str(&content);
                    las.other.push('\n');
                }
            },
            _ => {}
        }
    }
    
    // Final flush
    process_chunk(&line_chunk, &mut data_values, &mut ncols);
    
    // Assign data to curves
    if ncols > 0 && !data_values.is_empty() {
        let nrows = data_values.len() / ncols;
        let arr = Array2::from_shape_vec((nrows, ncols), data_values)?;
        
        for (i, (_key, curve)) in las.curves.items.iter_mut().enumerate() {
            if i < ncols {
                curve.data = arr.column(i).to_vec();
            }
        }
    }
    
    Ok(las)
}
