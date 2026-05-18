# AI Astrology Platform Architecture

## Overview
Scalable AI-powered astrology platform with separated concerns, modular services, and future extensibility for multi-agent reasoning and advanced chart types.

## Core Principles
- Separation of concerns: Frontend, Backend, Astrology Engine, AI Layer
- Modularity: Independent services that can be scaled separately
- Extensibility: Designed for future multi-agent systems and advanced divisional charts
- Performance: Optimized for fast chart generation and AI interpretation
- Maintainability: Clean folder structure with clear boundaries

## System Components

### 1. Frontend (Next.js)
```
frontend/
├── app/
│   ├── (dashboard)/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── charts/
│   │   │   ├── [chartType]/
│   │   │   │   ├── page.tsx
│   │   │   │   └── components/
│   │   │   │       ├── ChartViewer.tsx
│   │   │   │       ├── ChartControls.tsx
│   │   │   │       └── InterpretationPanel.tsx
│   │   ├── reports/
│   │   │   └── [reportId]/
│   │   │       ├── page.tsx
│   │   │       └── components/
│   │   ├── profile/
│   │   └── auth/
├── components/
│   ├── ui/
│   ├── charts/
│   │   ├── D1Chart.tsx
│   │   ├── D9Chart.tsx
│   │   └── BaseChart.tsx
│   ├── layout/
│   └── forms/
├── lib/
│   ├── api/
│   ├── utils/
│   └── charts/
├── hooks/
├── styles/
└── public/
```

### 2. Backend (FastAPI)
```
backend/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── dependencies.py
│   │   └── events.py
│   ├── api/
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── routes/
│   │   │   │   ├── charts.py
│   │   │   │   ├── interpretations.py
│   │   │   │   ├── reports.py
│   │   │   │   ├── users.py
│   │   │   │   └── health.py
│   │   │   ├── middleware/
│   │   │   └── deps.py
│   ├── services/
│   │   ├── chart_service.py
│   │   ├── interpretation_service.py
│   │   ├── report_service.py
│   │   └── user_service.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── chart.py
│   │   ├── interpretation.py
│   │   ├── report.py
│   │   └── user.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── chart.py
│   │   ├── interpretation.py
│   │   ├── report.py
│   │   └── user.py
│   ├── workers/
│   │   ├── celery_config.py
│   │   └── tasks/
│   │       ├── chart_generation.py
│   │       └── ai_interpretation.py
│   └── utils/
│       ├── logging.py
│       └── helpers.py
├── tests/
├── alembic/
└── requirements.txt
```

### 3. Astrology Engine (Separated Service)
```
astrology-engine/
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── calculator.py
│   │   ├── constants.py
│   │   └── exceptions.py
│   ├── charts/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── d1/
│   │   │   ├── __init__.py
│   │   │   ├── calculator.py
│   │   │   └── models.py
│   │   ├── d9/
│   │   │   ├── __init__.py
│   │   │   ├── calculator.py
│   │   │   └── models.py
│   │   └── divisional/  # Future divisional charts (D2, D3, D10, D16, D20, D24, D27, D30, D40, D45, D60)
│   │       ├── __init__.py
│   │       ├── base.py
│   │       └── [chart_type]/
│   │           ├── __init__.py
│   │           ├── calculator.py
│   │           └── models.py
│   ├── interpretations/
│   │   ├── __init__.py
│   │   ├── rules_engine.py
│   │   └── traditional/
│   │       ├── __init__.py
│   │       ├── d1.py
│   │       └── d9.py
│   ├── utils/
│   │   ├── coordinate.py
│   │   ├── house_calculations.py
│   │   └── aspects.py
│   └── api/
│       ├── __init__.py
│       ├── server.py  # gRPC or REST interface
│       └── models.py
├── tests/
├── requirements.txt
└── setup.py
```

### 4. AI Interpretation Layer
```
ai-layer/
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── prompt_manager.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── openai.py
│   │   ├── anthropic.py
│   │   └── local.py  # For future local model support
│   ├── services/
│   │   ├── __init__.py
│   │   ├── interpretation_generator.py
│   │   ├── context_enricher.py
│   │   └── quality_checker.py
│   ├── agents/  # Future multi-agent reasoning support
│   │   ├── __init__.py
│   │   ├── base_agent.py
│   │   ├── chart_analyst.py
│   │   ├── life_path_specialist.py
│   │   ├── relationship_analyst.py
│   │   └── career_advisor.py
│   ├── prompts/
│   │   ├── templates/
│   │   │   ├── d1.json
│   │   │   ├── d9.json
│   │   │   └── divisional/
│   │   │       └── [chart_type].json
│   │   └── dynamic/
│   │       ├── life_events.py
│   │       ├── relationships.py
│   │       └── career.py
│   └── utils/
│       ├── token_optimizer.py
│       └── safety_filters.py
├── tests/
├── requirements.txt
└── config/
    ├── models.yaml
    └── prompts.yaml
```

### 5. Database Layer (PostgreSQL)
```
Schema Design:
- users: id, email, password_hash, name, birth_data, created_at, updated_at
- charts: id, user_id, chart_type, planetary_positions, houses, aspects, generated_at
- interpretations: id, chart_id, ai_model_used, content, quality_score, created_at
- reports: id, user_id, title, chart_ids, generated_at, pdf_url
- report_shares: id, report_id, shared_with, expires_at, access_token
- api_keys: id, user_id, key_hash, name, is_active, last_used, created_at
- usage_analytics: id, user_id, endpoint, response_time, timestamp
```

### 6. Infrastructure & Deployment
```
infrastructure/
├── docker/
│   ├── backend.Dockerfile
│   ├── frontend.Dockerfile
│   ├── astrology-engine.Dockerfile
│   └── ai-layer.Dockerfile
├── kubernetes/
│   ├── namespace.yaml
│   ├── deployments/
│   │   ├── backend.yaml
│   │   ├── frontend.yaml
│   │   ├── astrology-engine.yaml
│   │   └── ai-layer.yaml
│   ├── services/
│   │   ├── backend-svc.yaml
│   │   ├── frontend-svc.yaml
│   │   ├── astrology-engine-svc.yaml
│   │   └── ai-layer-svc.yaml
│   ├── ingress/
│   │   └── frontend-ingress.yaml
│   ├── configmaps/
│   │   ├── backend-config.yaml
│   │   └── ai-layer-config.yaml
│   └── secrets/
│       ├── db-secret.yaml
│       └── api-keys.yaml
├── monitoring/
│   ├── prometheus/
│   └── grafana/
└── scripts/
    ├── setup.sh
    ├── deploy.sh
    └── backup.sh
```

## Data Flow & Workflows

### Chart Generation Workflow
1. User submits birth data via Next.js frontend
2. Frontend validates and sends to FastAPI `/charts/generate` endpoint
3. Backend validates request, stores initial chart record
4. Backend sends chart generation task to Astrology Engine via service API
5. Astrology Engine calculates planetary positions, houses, aspects
6. Results returned to backend, stored in database
7. Backend returns chart data to frontend for display

### AI Interpretation Workflow
1. After chart generation, frontend requests interpretation
2. Backend sends request to AI Interpretation Layer
3. AI Layer enriches chart data with life context (if available)
4. AI Layer generates interpretation using configured LLM
5. Optional: Quality check and safety filtering applied
6. Interpretation stored in database and returned to frontend
7. Frontend displays interpretation alongside chart

### Future Multi-Agent Reasoning Workflow
1. Chart data sent to AI Layer orchestrator
2. Orchestrator dispatches to specialized agents:
   - Chart Analyst: Technical chart analysis
   - Life Path Specialist: Career, purpose, life direction
   - Relationship Analyst: Compatibility, partnership patterns
   - Career Advisor: Professional strengths, timing, obstacles
3. Agents collaborate, share insights, build comprehensive interpretation
4. Orchestrator synthesizes agent outputs into cohesive report
5. Final interpretation stored and returned

## API Contracts

### Backend Endpoints
```
POST   /api/v1/charts/generate          # Generate new chart
GET    /api/v1/charts/{chart_id}        # Get chart data
GET    /api/v1/charts                   # List user charts
POST   /api/v1/interpretations/generate # Generate AI interpretation
GET    /api/v1/interpretations/{id}     # Get interpretation
POST   /api/v1/reports/generate         # Generate comprehensive report
GET    /api/v1/reports/{report_id}      # Get report
POST   /api/v1/reports/{id}/share       # Create shareable link
GET    /health                          # Health check
```

### Astrology Engine Service Interface
```
POST   /calculate/chart                  # Calculate chart from birth data
POST   /calculate/aspects               # Calculate planetary aspects
POST   /calculate/houses                # Calculate house cusps
GET    /chart-types                     # List supported chart types
GET    /health                          # Health check
```

### AI Layer Service Interface
```
POST   /interpret/chart                  # Generate interpretation for chart
POST   /enrich/context                  # Enrich chart with life context
GET    /models                          # List available AI models
POST   /quality/check                   # Check interpretation quality
GET    /health                          # Health check
```

## Scalability Considerations

### Horizontal Scaling
- Astrology Engine: Scale based on chart generation demand
- AI Layer: Scale based on interpretation request volume
- Backend: Scale based on API traffic
- Database: Use read replicas for heavy read workloads

### Caching Strategy
- Redis cache for frequently accessed charts
- Cache planetary calculations for common birth coordinates
- Cache AI interpretations for similar chart patterns
- Session caching for authenticated users

### Performance Optimization
- Asynchronous chart generation via Celery workers
- Batch processing for report generation
- Connection pooling for database connections
- Efficient algorithms for astrological calculations
- Pagination for large dataset queries

## Security Considerations
- Input validation at all API boundaries
- JWT-based authentication with refresh tokens
- Rate limiting per user/IP
- Data encryption at rest and in transit
- Regular security audits and penetration testing
- Secure API key management for external services
- GDPR-compliant data handling and deletion

## Extensibility Features

### Adding New Chart Types
1. Create new directory under `astrology-engine/src/charts/[chart_type]/`
2. Implement calculator.py with specific calculations
3. Define models.py for chart data structure
4. Register chart type in engine configuration
5. Add frontend component for visualization
6. Update API to accept new chart_type parameter

### Adding New AI Capabilities
1. Create new agent in `ai-layer/src/agents/[specialty].py`
2. Implement base agent interface
3. Register agent with orchestrator
4. Create prompt templates in `ai-layer/src/prompts/`
5. Update orchestration logic to include new agent
6. Add evaluation metrics for agent performance

### Integration Points
- Webhook support for external notifications
- Plugin system for custom interpretation modules
- API keys for third-party developer access
- Export functionality (PDF, JSON, image formats)
- Multi-language support through i18n

## Technology Stack Recommendations

### Frontend
- Next.js 13+ with App Router
- TypeScript for type safety
- Tailwind CSS for styling
- Chart.js or D3.js for chart visualization
- SWR or React Query for data fetching
- Zustand or Redux Toolkit for state management

### Backend
- FastAPI for high-performance API
- Python 3.9+
- SQLAlchemy ORM with PostgreSQL
- Celery for background tasks
- Redis for caching and message brokering
- Pydantic for data validation

### Astrology Engine
- Python 3.9+ for mathematical precision
- NumPy/Pandas for calculations
- Skyfield or PyEphem for astronomical computations
- gRPC or FastAPI for service interface
- Docker for containerization

### AI Layer
- LangChain or LlamaIndex for LLM orchestration
- Support for OpenAI, Anthropic, and local models
- Vector embeddings for context enrichment
- Prompt templating system
- Safety filters and content moderation

### DevOps
- Docker Compose for local development
- Kubernetes for production orchestration
- GitHub Actions for CI/CD
- Prometheus + Grafana for monitoring
- ELK stack for logging
- Sentry for error tracking