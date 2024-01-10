// From: https://huggingface.co/learn/nlp-course/chapter6/5?fw=pt (converted to Rust)
use indexmap::IndexMap; // used instead of HashMap to maintain insertion order
use tokenizers::{tokenizer::{Result, Tokenizer}, PreTokenizer, PreTokenizedString, OffsetReferential, OffsetType};

fn compute_pair_freqs(splits : &IndexMap<String, Vec<String>>, word_freqs: &IndexMap<String, i32>) -> IndexMap<(String,String), i32> {
    let mut pair_freqs = IndexMap::new();
    for (word, freq) in word_freqs {
        let split = splits.get(word).unwrap();
        if split.len() == 1{
            continue;
        }
        for i in 0..split.len()-1 {
            let pair = (split.get(i).cloned().unwrap(), split.get(i+1).cloned().unwrap());
            let count = pair_freqs.entry(pair).or_insert(0);
            *count += freq;
        }
    }
    pair_freqs
}

fn merge_pair(a: &String, b: &String, splits: &mut IndexMap<String, Vec<String>>, word_freqs: &IndexMap<String, i32>) {
    for word in word_freqs.keys() {
        let mut split = splits.get(word).unwrap().to_vec();
        if split.len() == 1 {
            continue;
        }
        let mut i = 0;
        while i < split.len() - 1 {
            let x = split.get(i).cloned().unwrap();
            let y = split.get(i+1).cloned().unwrap();
            if x == *a && y == *b {
                split.splice(i..i+2, [a.to_owned() + &b.to_owned()].iter().cloned()); 
            } else {
                i += 1;
            }
        }
        splits.insert(word.to_string(), split.to_vec());
        
    }
}

fn main() -> Result<()>{
    let tokenizer = Tokenizer::from_pretrained("gpt2", None)?;
    let corpus = [
        "This is the Hugging Face Course.",
        "This chapter is about tokenization.",
        "This section shows several tokenizer algorithms.",
        "Hopefully, you will be able to understand how they are trained and generate tokens.",
    ];
    if let Some(pre_tokenizer) = tokenizer.get_pre_tokenizer() {
        let mut word_freqs = IndexMap::new();
        for text in corpus {
            let mut pretoken = PreTokenizedString::from(text);
            pre_tokenizer.pre_tokenize(&mut pretoken)?;
            //println!("{:#?}", pretoken);
            let splits = pretoken.get_splits(OffsetReferential::Normalized, OffsetType::Byte);
            for split in splits {
                //println!("split is {}", split.0);
                let count = word_freqs.entry(String::from(split.0)).or_insert(0);
                *count += 1;
            }
        }
        println!("{:?}, {}", word_freqs, word_freqs.len());
        let mut alphabet:Vec<String> = Vec::new();
        for (word, _) in &word_freqs {
            for ch in word.chars() {
                let str = ch.to_string();
                if !alphabet.contains(&str) {
                    alphabet.push(str);
                }
            }
        }
        alphabet.sort();
        println!("{:?}", alphabet);

        alphabet.push(String::from("<|endoftext|>"));
        let mut vocab = alphabet;
        let mut splits: IndexMap<String, Vec<String>> = IndexMap::new();
        for word in word_freqs.keys() {
            let sp_word:Vec<_> = word.chars().map(|c| c.to_string()).collect();
            splits.insert(String::from(word), sp_word);
        }
        println!("{:?}", splits);

        let pair_freqs = compute_pair_freqs(&splits, &word_freqs);
        for (i, pair) in pair_freqs.keys().enumerate() {
            println!("{}, {:?}", i, pair);
            if i >= 5 {
                break
            }
        }

        let vocab_size = 50;
        let mut merges = IndexMap::new();
        while vocab.len() < vocab_size {
            let pair_freqs = compute_pair_freqs(&splits, &word_freqs);
            let mut best_pair = &(String::new(), String::new());
            let mut max_freq = 0;
            for (pair, freq) in &pair_freqs {
                if max_freq == 0 || max_freq < *freq {
                    best_pair = pair;
                    max_freq = *freq;
                }
            }
            merge_pair(&best_pair.0, &best_pair.1, &mut splits, &word_freqs);
            let combined = best_pair.0.to_owned() + &best_pair.1.to_owned();
            merges.insert(best_pair.clone(), combined.clone()); 
            vocab.push(combined);
        }
        println!("{:?}, {}", merges, merges.len());
        println!("{:?}", vocab);
        println!("{:?}, {}", vocab.sort(), vocab.len());

        let test = "This is not a token.";

        let mut pretoken = PreTokenizedString::from(test);
        pre_tokenizer.pre_tokenize(&mut pretoken)?;
        let splits = pretoken.get_splits(OffsetReferential::Normalized, OffsetType::Byte);
        let mut word_to_split: Vec<Vec<String>> = Vec::new();
        println!("splits is {:?}", splits);
        for split in splits {
            let sp_word:Vec<_> = split.0.chars().map(|c| c.to_string()).collect();
            word_to_split.push(sp_word);
        }
        let mut result = word_to_split.clone();
        for (pair, merge) in merges {
            println!("pair: {:?}, merge: {:?}", pair, merge);
            word_to_split = result.clone();
            for (idx, split) in word_to_split.iter_mut().enumerate() {
                let mut i = 0;
                while i < split.len() - 1 {
                    let a = split.get(i).cloned().unwrap();
                    let b = split.get(i+1).cloned().unwrap();
                    if a == pair.0 && b == pair.1 {
                        split.splice(i..i+2, [merge.clone()].iter().cloned());
                    } else {
                        i += 1;
                    }
                }
                result[idx] = split.to_vec();
            }
            println!("intermediate tokenized results {:?}", result);
        }
        println!("Tokenized results {:?}", result.iter().flatten().collect::<Vec<_>>());

    }
    Ok(())

}
