# ADR 0001: Model Routing and Semantic Caching Strategy for AI FinOps

## Context & Problem Statement
Deploying large language models (LLMs) at an enterprise scale introduces unpredictable operating costs driven by token volume consumption. Simple tasks—such as inbound client triage or simple semantic categorization—are often processed by standard high-cost commercial APIs (e.g., GPT-4, Claude 3.5 Sonnet), leading to significant financial overhead and computational inefficiency. 

Furthermore, repetitive or highly similar user queries execute redundant model inferences, causing unnecessary API expenses and latent processing delays. We need a strategy to minimize inference costs while maintaining high answer accuracy and low response latency.

---

## 🇧🇷 Decisão de Arquitetura (Resumo em Português)
**Status:** Approved
**Decisão:** Implementar uma infraestrutura combinada de **Roteamento Inteligente de Modelos (Model Routing)** e **Cache Semântico (Semantic Caching)** na camada central da aplicação (`src/core/`).

1. **Cache Semântico:** Utilizaremos o Redis estruturado com busca vetorial. Antes de enviar qualquer chamada de prompt para uma LLM externa, calcularemos o embedding da pergunta do usuário. Se o sistema encontrar um registro no cache com similaridade de cosseno superior a `0.92`, a resposta armazenada será retornada instantaneamente, resultando em custo zero de token e latência de sub-milissegundos.
2. **Model Routing Engine:** Caso ocorra um *cache miss*, o prompt será interceptado por um classificador leve de complexidade. Consultas de baixa complexidade serão roteadas para modelos locais de pequena escala (SLMs como Llama 3.2 3B ou Qwen 2.5 7B) rodando de forma isolada na nossa infraestrutura Docker via Ollama/vLLM. Consultas de alta complexidade analítica ou de múltiplas etapas serão elevadas para LLMs proprietárias robustas na nuvem.

### Consequências
* **Impacto Positivo:** Redução drástica e escalável de custos com APIs externas (FinOps), isolamento de requisições redundantes, e melhora significativa na latência geral do sistema.
* **Impacto Negativo:** Pequeno aumento na complexidade de manutenção do ecossistema e necessidade de gerenciar o ciclo de expiração e limpeza do banco de dados de cache.

---

## 🇺🇸 Architectural Decision (English Summary)
**Status:** Approved
**Decision:** Implement a structural system combining programmatic **Model Routing** and vector-based **Semantic Caching** inside the application's core framework (`src/core/`).

1. **Semantic Caching:** Leverage Redis vector-database capacities to cache historic prompt resolutions. Every new user payload will generate a vector embedding to scan historic states. If a cache vector registers a cosine similarity score above `0.92`, the application bypasses remote LLM networks and serving engines, returning the cached payload with near-zero latency and zero token billing.
2. **Model Routing Engine:** If a cache miss occurs, the runtime evaluates query complexity using a lightweight deterministic parsing layer. Tasks categorized as low-complexity are instantly pushed to self-hosted Small Language Models (SLMs like Llama 3.2 3B / Qwen 2.5 7B) managed internally via Ollama/vLLM. Complex orchestration pipelines, multi-step agents, or data transformations are conditionally routed to premium remote enterprise APIs.

### Consequences
* **Positive Impact:** Drastic reduction in commercial API bills (FinOps alignment), protection against redundant compute calls, and structural enhancements in average latency.
* **Negative Impact:** Marginal expansion of the core codebase complexity and the operational overhead required to tune token eviction policies within the cache layer.
