# ☕ → 🔷 Java to C# Code Translator

A desktop app that uses a fine-tuned AI model to automatically translate Java source code into C#.
Paste in your Java, click a button, get C#. That's it.

![App Screenshot](screenshot.png)

## 🌟 Highlights

- **No API key or internet connection needed after first run** — model is cached locally
- **Handles real syntax differences** — converts `ArrayList` to `IList`, `System.out.println` to `Console.WriteLine`, and more
- **Simple two-panel UI** — paste Java on the left, get C# on the right
- **Runs on CPU** — no GPU required

## ℹ️ Overview

Migrating a Java codebase to C# is a tedious, error-prone process. While the two languages share similar syntax and structure, there are enough differences — naming conventions, type systems, standard library calls — that manual translation is slow and frustrating.

This app uses a fine-tuned [CodeT5](https://huggingface.co/Salesforce/codet5-base) model trained on the [CodeXGLUE Code-to-Code Translation dataset](https://huggingface.co/datasets/google/code_x_glue_cc_code_to_code_trans) by Google, which contains thousands of paired Java and C# code samples. The model learns the structural and syntactic patterns that map between the two languages.

It's useful for developers working with legacy Java code, or anyone learning the differences between Java and C#.

## ⬇️ Installation
```bash
pip install torch transformers PyQt5 sentencepiece protobuf
```

Requires Python 3.8+. Developed and tested on Windows.

## 🚀 Usage
```bash
python app.py
```

Paste your Java code into the left panel and click **Translate Code**. The C# translation appears on the right.

> **Note:** The first run will download the model (~900MB) and cache it locally. Subsequent runs load instantly.

## 🔬 Examples

Each example shows the Java input, the expected C# output, and the actual model output.

---

**Example 1 — Simple method ✅**
```java
// Java Input
public String getProcessName(int id) {
    return "Process_" + id;
}
```
```csharp (expected output)
// (expected output)
public string GetProcessName(int id) {
    return "Process_" + id;
}
```
```csharp (actual output)
// (actual output)
public virtual string GetProcessName(int id) {
    return "Process_" + id;
}
```

---

**Example 2 — Type conversion ✅**
```java
// Java Input
public int listSize(ArrayList<String> list) {
    return list.size();
}
```
```csharp (expected output)
// (expected output)
public int ListSize(List<string> list) {
    return list.Count;
}
```
```csharp (actual output)
// (actual output)
public virtual int ListSize(IList<string> list) {
    return list.Count;
}
```

---

**Example 3 — Exception handling ⚠️**
```java
// Java Input
public void readFile(String path) {
    try {
        System.out.println("Opening: " + path);
    } catch (Exception e) {
        System.out.println("Error: " + e.getMessage());
    } finally {
        System.out.println("Done.");
    }
}
```
```csharp (expected output)
// (expected output)
public void ReadFile(string path) {
    try {
        Console.WriteLine("Opening: " + path);
    } catch (Exception e) {
        Console.WriteLine("Error: " + e.Message);
    } finally {
        Console.WriteLine("Done.");
    }
}
```
```csharp (actual output)
// (actual output)
// Note System.Out.WriteLine instead of Console.WriteLine
public virtual void ReadFile(string path) {
    try {
        System.Out.WriteLine("Opening: " + path);
    } catch (Exception e) {
        System.Out.WriteLine("Error: " + e.Message);
    } finally {
        System.Out.WriteLine("Done.");
    }
}
```

## ⚠️ Limitations

This is a small fine-tuned model and has some known shortcomings:

- Occasionally produces `System.Console.WriteLine` instead of `Console.WriteLine`
- May miss closing brackets on longer or more complex methods
- Works best on single methods rather than entire class files
- Output is not always perfectly formatted — minor cleanup may be needed

## 🤖 Model and Training

This app uses a fine-tuned version of [CodeT5](https://huggingface.co/Salesforce/codet5-base) by Salesforce, a pre-trained model designed for code understanding and generation tasks.

The model was fine-tuned on the [CodeXGLUE Code-to-Code Translation dataset](https://huggingface.co/datasets/google/code_x_glue_cc_code_to_code_trans) by Google to specialise in Java → C# translation.

Fine-tuned model: [vipinchaudhry/codet5-java-to-csharp-translation](https://huggingface.co/vipinchaudhry/codet5-java-to-csharp-translation)

Trained on a T4 GPU via Google Colab for 5 epochs (~1h 50min, 3220 training steps).
