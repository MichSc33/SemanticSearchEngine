
import jsonlines
with jsonlines.open("./AnnoCreator/test.jsonl", "r") as reader:
    line = next(iter(reader))
    print(f"filename: {line['filename']}\n")
    print("captions:")
    for i, caption in enumerate(line["captions"]):
        print(f"{i+1}) {caption}")