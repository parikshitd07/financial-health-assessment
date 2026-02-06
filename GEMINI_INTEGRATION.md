# Google Gemini 3 Flash Integration

## Overview

The Financial Health Assessment Tool now uses **Google Gemini 3 Flash** as the primary AI engine for financial analysis, offering superior performance at a fraction of the cost compared to other models.

## Why Gemini 3 Flash?

### Cost Efficiency
- **Gemini 3 Flash**: $0.50 per 1M input tokens / $3 per 1M output tokens
- **GPT-4**: Significantly more expensive
- **Claude 3**: Higher cost than Gemini

### Performance Benefits
- **Pro-level Intelligence**: Advanced reasoning capabilities at Flash speed
- **1M Token Context Window**: Analyze extensive financial documents
- **64k Output Tokens**: Generate comprehensive reports
- **Knowledge Cutoff**: January 2025 (most up-to-date)

### Advanced Features
- **Dynamic Thinking Levels**: Control reasoning depth and latency
- **Multimodal Support**: Process text, images, and structured data
- **JSON Mode**: Native structured output support

## Configuration

### Environment Variables

```env
# Primary AI Provider (Recommended)
GEMINI_API_KEY=your-gemini-api-key-here
AI_MODEL=gemini-3-flash-preview
GEMINI_THINKING_LEVEL=medium

# Optional Fallbacks
OPENAI_API_KEY=sk-your-openai-key  # Optional
CLAUDE_API_KEY=your-claude-key     # Optional
```

### Getting Your Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click "Get API Key"
4. Copy the generated key
5. Add to your `.env` file

## Thinking Levels

Gemini 3 Flash supports four thinking levels to balance speed vs. depth:

### Available Levels

1. **minimal** (Gemini 3 Flash only)
   - Fastest responses
   - Best for: Simple queries, high-throughput operations
   - Use case: Basic financial summaries, quick calculations

2. **low**
   - Minimizes latency and cost
   - Best for: Instruction following, chat, routine analysis
   - Use case: Standard financial assessments

3. **medium** (Default, Recommended)
   - Balanced thinking for most tasks
   - Best for: Comprehensive financial analysis
   - Use case: Full health assessments, recommendations

4. **high**
   - Maximum reasoning depth
   - Best for: Complex scenarios requiring deep analysis
   - Use case: Critical credit decisions, risk assessment

### How to Set

```python
# In .env file
GEMINI_THINKING_LEVEL=medium

# Or set dynamically in code
config = types.GenerateContentConfig(
    thinking_config=types.ThinkingConfig(
        thinking_level="medium"
    )
)
```

## Implementation Details

### AI Analysis Service

The system intelligently selects the AI provider:

```python
# Priority Order:
1. Gemini (if configured and model name contains "gemini")
2. GPT-4 (if configured and model name contains "gpt")
3. Claude (if configured and model name contains "claude")
4. Gemini (fallback if available)
5. GPT-4 (fallback if available)
```

### Gemini-Specific Features

```python
def _analyze_with_gemini(self, prompt: str) -> Dict[str, Any]:
    """Analyze using Google Gemini 3 Flash"""
    response = self.gemini_client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(
                thinking_level=settings.GEMINI_THINKING_LEVEL
            ),
            temperature=0.3,
            response_mime_type="application/json"  # Native JSON support
        )
    )
    
    result = json.loads(response.text)
    result["ai_model_used"] = self.model
    result["thinking_level"] = thinking_level
    return result
```

## Supported Models

### Gemini 3 Series

| Model | Context (In/Out) | Knowledge | Pricing* | Best For |
|-------|------------------|-----------|----------|----------|
| gemini-3-flash-preview | 1M / 64k | Jan 2025 | $0.50 / $3 | **Financial Analysis** (Recommended) |
| gemini-3-pro-preview | 1M / 64k | Jan 2025 | $2 / $12 | Complex scenarios |
| gemini-3-pro-image-preview | 65k / 32k | Jan 2025 | $2 / $0.134 per image | Document analysis |

*Pricing per 1M tokens

### Fallback Options

- **GPT-4**: Set `AI_MODEL=gpt-4` and `OPENAI_API_KEY`
- **Claude 3 Opus**: Set `AI_MODEL=claude-3-opus-20240229` and `CLAUDE_API_KEY`

## Use Cases

### 1. Financial Health Assessment
```python
# Uses Gemini 3 Flash with medium thinking level
assessment = ai_service.analyze_financial_health(
    financial_data=financial_data,
    business_info=business_info,
    industry_benchmarks=benchmarks
)
```

**Gemini Advantages**:
- Fast analysis of complex financial ratios
- Deep reasoning for credit scoring
- Cost-effective for high-volume assessments

### 2. Narrative Report Generation
```python
# Generate comprehensive reports
report = ai_service.generate_narrative_report(
    assessment=assessment,
    language="en"  # or "hi" for Hindi
)
```

**Gemini Advantages**:
- Large output tokens for detailed reports
- Multilingual support built-in
- Natural, professional writing style

### 3. Content Translation
```python
# Translate to regional languages
translated = ai_service.translate_content(
    content=report,
    target_language="hi"  # Hindi
)
```

**Gemini Advantages**:
- Superior multilingual capabilities
- Maintains financial terminology accuracy
- Cost-effective for bulk translations

## Performance Optimization

### Tips for Best Results

1. **Choose Right Thinking Level**
   - Use `minimal` for routine tasks
   - Use `medium` for standard analysis (default)
   - Use `high` only when critical

2. **Batch Requests**
   ```python
   # Analyze multiple businesses efficiently
   for business in businesses:
       assessment = analyze(business)  # Cost-effective with Flash
   ```

3. **Cache Responses**
   - Reuse analysis for similar businesses
   - Store industry benchmarks

4. **Monitor Usage**
   ```python
   # Track tokens and costs
   result["ai_model_used"]  # "gemini-3-flash-preview"
   result["thinking_level"]  # "medium"
   ```

## Cost Comparison

### Example: 100 Financial Assessments

Assumptions:
- Average input: 2,000 tokens per assessment
- Average output: 1,500 tokens per assessment

| Provider | Input Cost | Output Cost | Total Cost |
|----------|------------|-------------|------------|
| **Gemini 3 Flash** | $0.10 | $0.45 | **$0.55** |
| GPT-4 | ~$0.20 | ~$1.80 | **~$2.00** |
| Claude 3 Opus | ~$0.30 | ~$2.25 | **~$2.55** |

**Savings with Gemini**: 70-80% cost reduction!

## Error Handling

The system automatically falls back to alternative providers:

```python
try:
    # Try Gemini first
    result = _analyze_with_gemini(prompt)
except Exception as e:
    # Fall back to GPT-4 if available
    if self.openai_client:
        result = _analyze_with_gpt(prompt)
    # Or Claude
    elif self.claude_client:
        result = _analyze_with_claude(prompt)
```

## Best Practices

### 1. API Key Security
```bash
# Never commit API keys
echo ".env" >> .gitignore

# Use environment variables
export GEMINI_API_KEY="your-key-here"
```

### 2. Rate Limiting
```python
# Gemini has generous rate limits
# But implement rate limiting for safety
@limiter.limit("60/minute")
async def analyze_endpoint():
    ...
```

### 3. Error Handling
```python
try:
    result = ai_service.analyze_financial_health(data)
except Exception as e:
    logger.error(f"AI analysis failed: {str(e)}")
    # Handle gracefully
```

### 4. Monitoring
```python
# Log AI usage
logger.info(f"Analysis completed using {result['ai_model_used']}")
logger.info(f"Thinking level: {result.get('thinking_level', 'N/A')}")
```

## Migration from Other Providers

### From OpenAI GPT-4

```env
# Before
OPENAI_API_KEY=sk-...
AI_MODEL=gpt-4

# After (keep GPT as fallback)
GEMINI_API_KEY=your-key
AI_MODEL=gemini-3-flash-preview
OPENAI_API_KEY=sk-...  # Kept as fallback
```

### From Claude

```env
# Before
CLAUDE_API_KEY=...
AI_MODEL=claude-3-opus

# After
GEMINI_API_KEY=your-key
AI_MODEL=gemini-3-flash-preview
CLAUDE_API_KEY=...  # Kept as fallback
```

## Resources

- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [Google AI Studio](https://aistudio.google.com/)
- [Pricing Details](https://ai.google.dev/pricing)
- [Python SDK](https://github.com/google/generative-ai-python)

## Support

For Gemini-related issues:
1. Check [API Status](https://status.cloud.google.com/)
2. Review [Documentation](https://ai.google.dev/gemini-api/docs)
3. Contact Google AI Support
4. Check application logs: `docker-compose logs backend`

## Summary

Google Gemini 3 Flash provides:
- ✅ **70-80% cost savings** vs. GPT-4/Claude
- ✅ **Pro-level intelligence** at Flash speed
- ✅ **1M token context** for comprehensive analysis
- ✅ **Advanced reasoning** with thinking levels
- ✅ **Native JSON mode** for structured output
- ✅ **Multilingual support** for regional languages
- ✅ **Latest knowledge** (Jan 2025 cutoff)

**Recommended for**: Production deployment of Financial Health Assessment Tool
