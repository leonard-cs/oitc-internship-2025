**CLIP** (Contrastive Language-Image Pre-Training), which is a vision-language model developed by OpenAI. It’s designed to understand both images and text by mapping them into a shared vector space.
- `CLIPProcessor`: This is a utility class from the Transformers library. It helps preprocess the input images and text to make them compatible with the CLIP model. Essentially, it formats the images and text (like captions) in a way that CLIP can understand.
- `CLIPModel`: This is the pre-trained CLIP model. It contains the architecture for both the image encoder and the text encoder, which are used to create embeddings for the respective input (image or text).

## Vector database
I want the database to be hybrid support(image + text) and docker friendly. I tried Weaviate but it's too complicate to setup.
| Vector DB        | Self-Host   | Hybrid (Text+Image)               | Docker       | Complexity      | Notes                                         |
| ---------------- | ----------- | --------------------------------- | ------------ | --------------- | --------------------------------------------- |
| **Qdrant**       | ✅ Yes       | ✅ Native multimodal               | ✅ Easy       | ⭐ Low           | 🥇 Best all-rounder (easy, fast, accurate)    |
| **Weaviate**     | ✅ Yes       | ✅ Text+Image+RAG                  | ✅ Medium     | Medium          | Full-featured, RESTful, supports modules      |
| **Milvus**       | ✅ Yes       | ✅ Yes (via embeddings)            | ✅ Hard       | 😵 High         | High perf but complex (requires etcd, pulsar) |
| **Chroma**       | ✅ Yes       | 🟡 Text-focused                   | ✅ Easy       | ⭐ Easy          | Great for small setups, no hybrid search      |
| **PGVector**     | ✅ Yes       | 🟡 Manual hybrid                  | ✅ Easy       | ⭐ Easy          | Embeddings stored in Postgres arrays          |
| **LanceDB**      | ✅ Yes       | 🟡 Needs manual logic             | ✅ Easy       | ⭐ Easy          | Embedded-style (like DuckDB for vectors)      |
| **Pinecone**     | ❌ No        | ✅ Yes                             | ❌ Cloud only | –               | Expensive, cloud-only                         |
| **Zilliz Cloud** | ❌ No        | ✅ Yes                             | ❌ Cloud only | –               | Milvus Cloud — closed + \$\$                  |
| **AstraDB**      | ✅ (limited) | 🟡 Text only (Cassandra + vector) | 🟡           | ❗Limited hybrid | Good if already in Cassandra ecosystem        |
