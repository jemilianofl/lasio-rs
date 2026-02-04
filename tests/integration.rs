use lasio_rs::reader::parse_las_from_reader;
use std::fs::File;
use std::io::BufReader;

#[test]
fn test_read_sample_las() {
    let file = File::open("sample.las").expect("Failed to open sample.las");
    let reader = BufReader::new(file);
    let las = parse_las_from_reader(reader).expect("Failed to parse LAS");

    // Check Version
    assert_eq!(las.version.items.get("VERS").unwrap().value, "2.0");
    assert_eq!(las.version.items.get("WRAP").unwrap().value, "NO");

    // Check Well
    assert_eq!(las.well.items.get("STRT").unwrap().value, "1670.0000");
    assert_eq!(las.well.items.get("STOP").unwrap().value, "1669.7500");
    assert_eq!(las.well.items.get("STEP").unwrap().value, "-0.1250");
    assert_eq!(las.well.items.get("NULL").unwrap().value, "-999.25");

    // Check Curves Metadata
    assert!(las.curves.items.contains_key("DEPT"));
    assert!(las.curves.items.contains_key("DT"));

    // Check Data
    // DEPT column 0
    let dept_curve = las.curves.items.get("DEPT").unwrap();
    assert_eq!(dept_curve.data.len(), 3);
    assert!((dept_curve.data[0] - 1670.0000).abs() < 1e-4);
    assert!((dept_curve.data[1] - 1669.8750).abs() < 1e-4);
    assert!((dept_curve.data[2] - 1669.7500).abs() < 1e-4);

    // DT column 1
    let dt_curve = las.curves.items.get("DT").unwrap();
    assert_eq!(dt_curve.data.len(), 3);
    assert!((dt_curve.data[0] - 123.45).abs() < 1e-4);
    assert!((dt_curve.data[1] + 999.25).abs() < 1e-4); 
    assert!((dt_curve.data[2] - 124.50).abs() < 1e-4);
}
