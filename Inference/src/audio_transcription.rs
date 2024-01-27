fn fahrenheit_to_celsius(value: f32) -> f32{
    (value-32)/(9f32/5f32)
}

fn nth_fibonnaci(position: u32){
    let mut numbers: Vec<u32> = vec![0, 1];
    while numbers.len() <= position{
        numbers.push(numbers[numbers.len()-1] + numbers[numbers.len()-2]);
    }
    numbers[position]
}