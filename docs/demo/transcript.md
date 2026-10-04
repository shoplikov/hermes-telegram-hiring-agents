# Demo transcript — TASK#4 (2026-10-01, real posting)

Request: Senior AI Engineer, NJSC "Social Health Insurance Fund" (Astana), pasted by the user in the "Job War Room" group with `@alish_hr_coordinator_bot`.
Reconstructed from the three agents' `state.db` session stores and gateway logs. CV used: v2.

## Timeline

| Time | From → To | Message |
|---|---|---|
| 14:47:55 | user → coordinator | posting text (≈1.5k chars) |
| 14:48:09 | coordinator → scout + analyst | plan + `@alish_company_scout_bot TASK#4 research …` + `@alish_cv_analyst_bot TASK#4 assess fit …` |
| 14:48:25 | analyst → coordinator | `RESULT#4` fit 60/100, requirement table, top gaps |
| 14:48:26 | scout → coordinator | `RESULT#4` company, stack, news, interview process, red flags, sources |
| 14:48:34 | coordinator → analyst | `TASK#4 tailor 3-6 CV bullets … using this company context` (should have been `TASK#4b`, see failures #6) |
| 14:48:41 | analyst → coordinator | tailored bullets |
| 14:48:46 | coordinator → analyst | **duplicate** tailoring request from a second coordinator session (failures #5) |
| 14:48:54 | analyst → coordinator | bullets again |
| 14:48:58 | coordinator → user | 📋 final brief |
| 14:49:06 | coordinator → user | **duplicate** final brief (failures #5) |

Total wall time: ~70 s from posting to brief. Both duplicates were caused by per-sender sessions and are fixed (see `docs/failures.md` #5).

## Key messages (verbatim)

### 14:48:09 — Hiring Coordinator
I’m opening TASK#4 for this role: I’ll get company context and check your fit, then I’ll prepare the tailored brief.

@alish_company_scout_bot TASK#4 research NJSC “Social Health Insurance Fund” for a Senior AI Engineer application. Focus: product, tech stack, team/culture, recent news (12 months), interview process reports, red flags. Return sources.

@alish_cv_analyst_bot TASK#4 assess fit for Senior AI Engineer at NJSC “Social Health Insurance Fund”. MUST: 3+ years developing AI/LLM solutions; proficiency in Python, PyTorch, Transformers, and Hugging Face; hands-on LLM fine-tuning with LoRA/QLoRA, PEFT, or SFT; RAG experience with embeddings, vector databases, reranking, and retrieval evaluation; knowledge of LangChain, LlamaIndex, or similar frameworks; experience with APIs, Docker, Git, Linux, and GPU infrastructure; understanding of hallucinations, context limits, security, and quality control. NICE: none specified. Context: Astana, on-site; medical insurance system operator; internal AI tasks, assistants, and intelligent search.

### 14:48:26 — Company Scout
@alish_hr_coordinator_bot RESULT#4
**Company:** The Social Health Insurance Fund (FSSMS) is Kazakhstan’s state operator for compulsory social health insurance, managing healthcare financing, provider settlements, citizen services and related national information systems.

**Stack:** Publicly documented systems include a Situational-Analytical Center combining data from 18 databases, with 1,000+ dashboards and about 500 indicators; reported tools include Power BI, Superset and QlikSense, with planned integration across 26 information systems. The vacancy adds Python, PyTorch, Transformers, Hugging Face, LoRA/QLoRA, PEFT/SFT, embeddings, vector DBs, reranking, RAG, LangChain/LlamaIndex, APIs, Docker, Git, Linux and GPU infrastructure. The exact internal LLM platform and deployment architecture are **unverified**.

**Team/culture:** Public-sector, healthcare and data-governance environment. Expect strict requirements around personal/medical data, access control, audit trails, explainability, uptime and human review. The role likely works across IT, analytics, healthcare operations, security, legal and government stakeholders. Delivery may be formal and procurement-dependent; **unverified**.

**Recent news:**  
- The Fund reported preparation for a transition to a new public-administration model after the first half of 2026.  
- A January 2026 government inspection was reported as finding systemic violations and low efficiency; separate reporting described an investigation into alleged embezzlement. These reports require careful verification and are significant organizational context.  
- In 2025, the government instructed the Ministry of Healthcare and Fund to automate business processes and relaunch the digital platform, including AI/digital tools.  
- The analytics center remains a major modernization asset for healthcare-financing and service-quality oversight.

**Interview process:** No reliable FSSMS-specific AI-engineer interview reports found. **Unverified likely process:** HR screening, technical panel, LLM/RAG architecture exercise, security/privacy review and leadership interview. Prepare a design for a multilingual internal assistant with permission-aware retrieval, hybrid search, reranking, citations, retrieval/answer evaluation, PII controls, prompt-injection defenses, monitoring and rollback.

**Red flags:**  
- Organizational/governance transition and 2026 audit/investigation reports—ask what changed, who owns AI and how stable the team/budget is.  
- Gross salary is below the headline net amount; calculate the expected take-home pay.  
- Confirm GPU availability, approved open-source models, whether data must stay inside Kazakhstan/government infrastructure, security-approval timelines, on-call duties and deployment authority.  
- Clarify whether “Senior AI Engineer” means platform ownership, individual delivery or modernization under an existing vendor.

**Sources:**  
- https://msqory.kz/ru/press-tsentr/news/detail.php?ELEMENT_ID=492800  
- https://qazinform.com/news/kazakhstan-audit-exposes-massive-violations-in-social-health-insurance-fund-dea675  
- https://primeminister.kz/en/news/implementation-of-the-presidents-instructions-on-modernization-of-compulsory-social-health-insurance-system-government-is-modernizing-the-health-insurance-system-using-artificial-intelligence-30580  
- https://tekelinews.kz/news/cat-7/15939/  
- https://p4h.world/en/news/social-health-insurance-fund-ceo-presents-newly-launched-data-analytics-tools/  
- https://msqory.kz/ru/eshche/vakansii/

### 14:48:58 — Hiring Coordinator
📋 **Application brief — Senior AI Engineer @ NJSC “Social Health Insurance Fund”** (TASK#4)

**Fit:** 60/100 — highly relevant production RAG, LangGraph, vector-search, API, CI/CD, and GPU-serving experience; required seniority, LLM fine-tuning, Linux, and safety/security evidence are missing or incomplete.

**You meet:**  
✅ Python, PyTorch, Transformers, Hugging Face  
✅ RAG, embeddings, vector DBs, reranking, retrieval evaluation  
✅ LangChain / LangGraph-style frameworks  
✅ APIs, Docker, Git, GPU infrastructure  
✅ Traceable, regulated-domain workflow design

**Partially:**  
🟡 3+ years developing AI/LLM solutions  
🟡 Linux evidence  
🟡 Hallucinations / context limits / security / quality control  
**Missing:**  
❌ Hands-on LLM fine-tuning with LoRA/QLoRA, PEFT, or SFT  
❌ 3+ years explicitly evidenced

**About the company:**  
The Fund is Kazakhstan’s state operator for compulsory social health insurance, managing healthcare financing, provider settlements, citizen services, and national information systems.  
Public systems include a Situational-Analytical Center combining data from 18 databases, with 1,000+ dashboards and about 500 indicators; reported tools include Power BI, Superset, and QlikSense.  
The role sits in a public-sector, healthcare, and data-governance environment with strict security, privacy, audit trails, explainability, and human review.  
**Red flag:** audit/investigation reporting and a public-administration transition mean you should verify stability, authority, and deployment ownership.

**Tailored CV bullets:**  
- Architected a multi-tenant, cited-answer AI platform combining PostgreSQL, Redis, Qdrant, OpenSearch, MinIO, MCP tooling, and a LangGraph runtime—well suited to traceable internal-assistant workflows across complex information systems.  
- Built a Kazakh/Russian legal RAG chatbot using E5 embeddings, Qdrant, OpenSearch BM25, RRF fusion, and HyDE; streamed answers with citations to support explainability in regulated contexts.  
- Developed ingestion and semantic-search tooling for 600+ SQL-sourced case documents, including a per-agent BGE reranker control for runtime retrieval-precision tuning.  
- Automated administrative-case compliance review by validating penalties and procedural deadlines against versioned legal codes; reduced LLM context by ~75% using Qdrant field filtering and PostgreSQL checkpointing.  
- Deployed PostgreSQL, Redis, Qdrant, OpenSearch, and MinIO via Docker Compose and GitLab CI/CD on a 4-GPU server serving Qwen3.8-27B with vLLM tensor parallelism.  
- Benchmarked inference engines on an NVIDIA DGX Spark test node, improving Qwen3.8-27B serving to 48 tok/s with SGLang, NVFP4, and DFlash2 speculative decoding while retaining lossless output.

**Likely interview questions (5):**  
1. How would you design an internal assistant for sensitive healthcare-finance data with access control and audit logs?  
2. How do you evaluate retrieval quality, groundedness, and hallucinations in a regulated RAG system?  
3. What safeguards would you add for PII, prompt injection, and unsafe model outputs?  
4. How would you deploy and monitor GPU-backed AI services in a public-sector environment?  
5. Describe a time you reduced context, latency, or cost without harming answer quality.

**Questions to ask them (3):**  
1. What data sources are in scope, and what access restrictions apply?  
2. Who approves model deployment and what security review is required?  
3. Is the role expected to own fine-tuning, or primarily retrieval and internal-assistant development?

**Next steps:**  
- Reframe the CV around regulated-domain RAG, auditability, and production ownership.  
- Add truthful Linux and fine-tuning evidence if you have it; otherwise don’t overstate them.  
- Prepare a short security-first system design for internal assistants over sensitive data.

