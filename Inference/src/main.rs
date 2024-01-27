use cpal::traits::{DeviceTrait, HostTrait, StreamTrait};
use rubato::{Resampler, SincFixedIn, InterpolationType, InterpolationParameters};
use whisper_rs::{FullParams, SamplingStrategy, WhisperContext, WhisperContextParameters, WhisperState};
use std::sync::{Arc, Mutex};
use anyhow::anyhow;
use std::fs::File;
use std::io::Write;

struct Transcriber{
    ctx: WhisperContext,
}

impl Transcriber {
    fn new() -> Self {
        let mut params = WhisperContextParameters::new();
        params.use_gpu(true);
        let ctx = WhisperContext::new_with_params("data/models/whisper/ggml-model-whisper-base.en-q5_1.bin", params).expect("Failed to create context.");
        Self {
            ctx
        }
    }

    fn transcribe(&self, vec: Vec<f32>) {
        let mut state = self.ctx.create_state().expect("Failed to create state.");

        let mut params = FullParams::new(SamplingStrategy::Greedy{best_of: 1});

        params.set_n_threads(8);
        params.set_translate(true);
        params.set_language(Some("en"));
        params.set_print_special(false);
        params.set_print_progress(false);
        params.set_print_realtime(false);
        params.set_print_timestamps(false);

        println!("Running model...");
        state
            .full(params, &vec[..])
            .expect("failed to run model");

        // fetch the results
        let num_segments = state
            .full_n_segments()
            .expect("failed to get number of segments");
        println!("Number of segments: {}", num_segments);
        for i in 0..num_segments {
            let segment = state
                .full_get_segment_text(i)
                .expect("failed to get segment");
            let start_timestamp = state
                .full_get_segment_t0(i)
                .expect("failed to get segment start timestamp");
            let end_timestamp = state
                .full_get_segment_t1(i)
                .expect("failed to get segment end timestamp");
            println!("[{} - {}]: {}", start_timestamp, end_timestamp, segment);
        }
        print!("Transcribed!");
    }
}

use hound;
fn save_buffer_to_wav(buffer: &[f32], file_path: &str, sample_rate: u32) -> hound::Result<()> {
    let spec = hound::WavSpec {
        channels: 1,
        sample_rate,
        bits_per_sample: 32,
        sample_format: hound::SampleFormat::Float,
    };

    let mut writer = hound::WavWriter::create(file_path, spec)?;
    for &sample in buffer {
        writer.write_sample(sample)?;
    }

    writer.finalize()?;
    Ok(())
}

fn main() -> Result<(), anyhow::Error> {
    let transcriber = Transcriber::new();

    let host = cpal::default_host();
    let device = host.default_input_device().ok_or(anyhow!("Failed to get default input device"))?;

    // Get the supported formats

    let stream_config = cpal::StreamConfig {
        channels: 1,
        sample_rate: cpal::SampleRate(16000),
        buffer_size: cpal::BufferSize::Default,
    };

    let buffer =  Arc::new(Mutex::new(Vec::new()));
    let buffer_size = 60000; // 16kHz

    let buffer_clone = Arc::clone(&buffer);
    let stream = device.build_input_stream(
        &stream_config,
        move |data: &[f32], _: &cpal::InputCallbackInfo| {
            let mut buffer = buffer_clone.lock().unwrap();
            buffer.extend_from_slice(data);
            if buffer.len() >= buffer_size {
                println!("Buffer full, transcribing.");
                // Process the audio chunk.
                transcriber.transcribe(buffer.clone());
                // Clear the buffer or handle overlapping.
                if let Err(e) = save_buffer_to_wav(&buffer, "output.wav", 16000) {
                    eprintln!("Failed to save buffer to WAV file: {}", e);
                }
                buffer.clear();
            }
        },
        move |err| {
            eprintln!("An error occurred on the input audio stream: {}", err);
        },
    )?;

    stream.play()?;
    // Keep the thread alive while the stream is being processed.
    loop {
        std::thread::sleep(std::time::Duration::from_millis(50));
    }
}
