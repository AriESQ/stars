
<a href="https://discord.gg/w2Ejj36hRU">
  <img src="https://user-images.githubusercontent.com/31022056/158916278-4504b838-7ecb-4ab9-a900-7dc002aade78.png" alt="Join us on Discord" width="200px">
</a>

# Documind

**`Documind`** is an advanced document processing tool that leverages AI to extract structured data from PDFs. It is built to handle PDF conversions, extract relevant information, and format results as specified by customizable schemas.

## **Features**

- Extracts structured JSON output from unstructured documents.
- Converts documents into Markdown format.
- Supports custom schemas for data extraction.
- Includes pre-defined templates for common schemas.
- Works with OpenAI and custom LLM setups (Llava and Llama3.2-vision).
- Auto-generates schemas based on document content.

### Try the Hosted Version 🚀

The hosted version provides a seamless experience with fully managed APIs, so you can skip the setup and start extracting data right away. [Join the beta](https://documind.xyz) to get access to the hosted service. 

## Roadmap

### ✅ Released Features  
- [x] PDF Extraction  
- [x] Basic Schema Definition  
- [x] Structured JSON Output  
- [x] Template Schemas  
- [x] Local LLM Integration (Llama3.2)  
- [x] Auto-generated Schemas  
- [x] Document Formatters (Text and Markdown)  
- [x] Multi-file Support (DOCX, PNG, JPG, TXT, HTML)  
- [x] Additional Schema Field Types (Boolean and Enum)

### 🚧 Upcoming Features  
- [ ] Additional Models (Local and cloud)  
- [ ] Image Extraction  
- [ ] Advanced Document Formatters  
- [ ] Data Classification
- [ ] Use Your Fine-tuned Models

## **Requirements**

Before using **`documind`**, ensure the following software dependencies are installed:

### **System Dependencies**

- **Ghostscript**: **`documind`** relies on Ghostscript for handling certain PDF operations.
- **GraphicsMagick**: Required for image processing within document conversions.

Install both on your system before proceeding:

```bash
# On macOS
brew install ghostscript graphicsmagick

# On Debian/Ubuntu
sudo apt-get update
sudo apt-get install -y ghostscript graphicsmagick

```

### **Node.js & NPM**

Ensure Node.js (v18+) and NPM are installed on your system.

## **Installation**

You can install **`documind`** via npm:

```bash
npm install documind

```

### **Environment Setup**

**`documind`** requires an **`.env`** file to store sensitive information like your OpenAI API key.

Create an **`.env`** file in your project directory and add the following:

```bash
OPENAI_API_KEY=your_openai_api_key
```

## **Usage**

### **Basic Example**

First, import **`documind`** and define your schema. The schema outline what information **`documind`** should look for in each document. Here’s a quick setup to get started.

### **1. Define a Schema**

The schema is an array of objects where each object defines:

- **name**: Field name to extract.
- **type**: Data type (e.g., **`"string"`**, **`"number"`**, **`"array"`**, **`"object"`**).
- **description**: Description of the field.
- **children** (optional): For arrays and objects, define nested fields.

Example schema for a bank statement:

```jsx
const schema = [
  {
    name: "accountNumber",
    type: "string",
    description: "The account number of the bank statement."
  },
  {
    name: "openingBalance",
    type: "number",
    description: "The opening balance of the account."
  },
  {
    name: "transactions",
    type: "array",
    description: "List of transactions in the account.",
    children: [
      {
        name: "date",
        type: "string",
        description: "Transaction date."
      },
      {
        name: "creditAmount",
        type: "number",
        description: "Credit Amount of the transaction."
      },
      {
        name: "debitAmount",
        type: "number",
        description: "Debit Amount of the transaction."
      },
      {
        name: "description",
        type: "string",
        description: "Transaction description."
      }
    ]
  },
  {
    name: "closingBalance",
    type: "number",
    description: "The closing balance of the account."
  }
];

```

### **2. Run `documind`**

Use **`documind`** to process a PDF by passing the file URL and the schema.

```jsx
import { extract } from 'documind';

const runExtraction = async () => {
  const result = await extract({
    file: 'https://bank_statement.pdf',
    schema
  });

  console.log("Extracted Data:", result);
};

runExtraction();

```

### **Example Output**

Here’s an example of what the extracted result might look like:

```json
 {
  "success": true,
  "pages": 1,
  "data": {
    "accountNumber": "100002345",
    "openingBalance": 3200,
    "transactions": [
        {
        "date": "2021-05-12",
        "creditAmount": null,
        "debitAmount": 100,
        "description": "transfer to Tom" 
      },
      {
        "date": "2021-05-12",
        "creditAmount": 50,
        "debitAmount": null,
        "description": "For lunch the other day"
      },
      {
        "date": "2021-05-13",
        "creditAmount": 20,
        "debitAmount": null,
        "description": "Refund for voucher"
      },
      {
        "date": "2021-05-13",
        "creditAmount": null,
        "debitAmount": 750,
        "description": "May's rent"
      }
    ],
    "closingBalance": 2420
  },
  "fileName": "bank_statement.pdf"
}

```

Read the [documentation](https://docs.documind.xyz/guides/schema-definition) for more on how to define schemas and and enable auto-generation.

### **Templates**

Documind comes with built-in templates for extracting data from popular document types like invoices, bank statements, and more. These templates make it easier to get started without defining your own schema.

**List available templates**

You can list all available templates using the `templates.list` function.

```javascript
import { templates } from 'documind';

const templates = templates.list();
console.log(templates); // Logs all available template names
```
**Use a template**

To use a template, simply pass its name to the `extract` function along with the file you want to extract data from. Here's an example:

```javascript
import { extract } from 'documind';

const runExtraction = async () => {
  const result = await extract({
    file: 'https://bank_statement.pdf',
    template: 'bank_statement'
  });

  console.log("Extracted Data:", result);
};

runExtraction();
```
Read the [templates documentation](https://docs.documind.xyz/templates/overview) for more details on templates and how to contribute yours.

## **Using Local LLM Models**

Read more on how to use local models [here](https://docs.documind.xyz/guides/local-models).

## **Contributing**

Contributions are welcome! Please submit a pull request with any improvements or features.

## **License**

This project is licensed under the AGPL v3.0 License.

## **Credit**

This repo was built on top of [Zerox](https://github.com/getomni-ai/zerox). The MIT license from Zerox is included in the core folder and is also mentioned in the root license file.

---
