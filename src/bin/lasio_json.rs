use _lasio_rs::reader::parse_las_from_reader;
use std::env;
use std::fs::File;
use std::io::BufReader;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: lasio_json <file.las>");
        std::process::exit(1);
    }
    let file = File::open(&args[1]).expect("Failed to open file");
    let reader = BufReader::new(file);
    match parse_las_from_reader(reader) {
        Ok(las) => {
             println!("{}", serde_json::to_string_pretty(&las).expect("Failed to serialize"));
        },
        Err(e) => {
            eprintln!("Error parsing LAS: {}", e);
            std::process::exit(1);
        }
    }
}
