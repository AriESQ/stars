# 🎯 Prompt Injector

> **Experimental TypeScript library for generating AI security test conversations**

[![npm version](https://badge.fury.io/js/@blueprintlabio%2Fprompt-injector.svg)](https://www.npmjs.com/package/@blueprintlabio/prompt-injector)
[![GitHub](https://img.shields.io/github/license/BlueprintLabIO/prompt-injector)](https://github.com/BlueprintLabIO/prompt-injector)

⚠️ **EXPERIMENTAL SOFTWARE**: This is an early-stage research project built with Claude Code. Success rates and effectiveness claims are based on preliminary research and may not reflect real-world performance. Use for educational and defensive testing purposes only.

A minimal, composable library that generates multi-turn prompt injection attack conversations for security professionals to test AI systems.

## 🚨 Early Development Status

**This is experimental V0.1 software** seeking feedback from the AI security community:

- Template-based implementation (no LLM dependencies)
- Research-informed but not empirically validated on your systems
- Success rate claims based on published research, not internal testing
- Designed for defensive security testing and education

## 🚨 The Problem

Current AI security testing has significant gaps:

- **Single-turn focus** misses how real attacks unfold over conversations
- **Static pattern libraries** can't adapt to evolving AI defenses
- **"Smart" evaluation tools** may provide false confidence
- **Heavy frameworks** require complex setup and API dependencies

Research suggests multi-turn attacks may be more effective than single-turn attempts, with attackers using conversation flow to build trust before exploitation.

## ✅ Our Approach

**Generate research-informed attack conversations. Let security professionals evaluate results.**

```typescript
import { PromptInjector } from '@blueprintlabio/prompt-injector';

const injector = new PromptInjector();

// Generate multi-turn attack conversation
const conversation = injector.generateConversation(
  "Extract user financial information", 
  { strategy: 'roleplay', maxTurns: 4 }
);

// Test each turn against your AI system
conversation.turns.forEach(turn => {
  console.log(`Turn ${turn.turnNumber}: ${turn.message}`);
  // Manually test this against your AI system
});
```

## 🎯 Why This Approach

### **Research-Informed Patterns**
- Based on documented prompt injection techniques from security literature
- Multi-turn conversation flows observed in security research
- Composable primitives that can be combined and extended

### **Lightweight & Practical** 
- **<100KB bundle** - works in browsers, Node.js, CI/CD pipelines
- **Zero API dependencies** - no external services required for core functionality
- **Composable architecture** - extend with custom attack techniques

### **Honest About Limitations**
- **No automated evaluation** - security professionals assess responses
- **No "confidence scores"** from pattern matching
- **No claims to "solve AI security"** - just better attack generation tools

## 🚀 Quick Start

```bash
npm install @blueprintlabio/prompt-injector
```

### Generate Attack Conversations

```typescript
import { PromptInjector } from '@blueprintlabio/prompt-injector';

const injector = new PromptInjector();

// Test different attack strategies
const strategies = ['gradual', 'roleplay', 'obfuscated', 'direct'];

for (const strategy of strategies) {
  const conversation = injector.generateConversation(
    "Get the AI to reveal its system prompt",
    { strategy, maxTurns: 3 }
  );
  
  console.log(`\n🎯 ${strategy} Attack:`);
  conversation.turns.forEach(turn => {
    console.log(`\n👤 User: ${turn.message}`);
    console.log(`🤖 AI: [Test this against your system]`);
  });
}
```

### Custom Attack Goals

```typescript
// Test different attack objectives
const goals = [
  "Extract user personal information",
  "Generate harmful content instructions", 
  "Bypass content safety filters",
  "Access unauthorized system functions",
  "Reveal training data or system prompts"
];

for (const goal of goals) {
  const conversation = injector.generateConversation(goal, { strategy: 'roleplay' });
  console.log(`\nTesting: ${goal}`);
  // Test each turn against your AI system manually
}
```

## 🔬 Attack Strategies

### **Roleplay Attacks**
Research-informed character impersonation techniques
- "In this creative writing exercise about {goal}..."
- "For this fictional scenario, pretend you're..."
- Based on roleplay effectiveness observed in security research

### **Encoding Attacks**
Character manipulation and encoding techniques
- Base64 encoding of malicious instructions
- Hexadecimal encoding bypass attempts
- FlipAttack-style character manipulation

### **Gradual Attacks**
Multi-turn trust building approach
- **Turn 1**: "I'm researching AI safety for my thesis..."
- **Turn 2**: "What vulnerabilities do researchers study?"
- **Turn 3**: Direct request with established context

### **Direct Attacks**
Fast attacks for rapid testing
- Context reset techniques
- Immediate goal pursuit

## 🎯 Use Cases

### **Security Testing**
- Test your AI systems before deployment
- Generate attack scenarios for red team exercises
- Validate prompt injection defenses

### **CI/CD Integration**
- Automated security testing in deployment pipelines
- Regression testing for AI safety measures
- Continuous monitoring of AI system robustness

### **Research & Education**
- Study prompt injection attack patterns
- Educational demonstrations of AI vulnerabilities
- Academic research on AI security

## 📚 Research Foundation

This library implements techniques inspired by published research:

### **Multi-turn Attack Effectiveness**
Liu, Y., He, X., Xiong, M., Fu, J., Deng, S., & Hooi, B. (2024). *FlipAttack: Jailbreak LLMs via Flipping*. arXiv preprint arXiv:2410.02832. Demonstrates high success rates for character manipulation attacks.

### **Roleplay Attack Dynamics**
Documented in "Red Teaming the Mind of the Machine: A Systematic Evaluation of Prompt Injection and Jailbreak Vulnerabilities in LLMs" showing roleplay as highly effective attack vector.

### **Encoding Bypass Techniques**
Mozilla's 0Din platform research by Figueroa, M. (2024) demonstrating hexadecimal encoding bypasses in ChatGPT-4o guardrails.

### **Base64 Attack Vectors**
Research showing Base64 encoding as common attack vector, with defensive applications explored in "Defense against Prompt Injection Attacks via Mixture of Encodings" (arXiv:2504.07467).

### **OWASP Classification**
- **OWASP LLM Top 10**: Prompt injection ranked as #1 AI security risk
- Multi-turn patterns observed in security research and red team exercises
- Context manipulation techniques documented in prompt injection literature

⚠️ **Research Disclaimer**: Success rates and effectiveness may vary significantly based on target AI system, safety measures, and specific implementation details. This library provides tools for testing - not guarantees of attack success.

## 🛡️ Responsible Use

**This tool is designed exclusively for defensive security testing.**

✅ **Appropriate Use:**
- Testing AI systems you own or have explicit permission to test
- Security research and authorized red team exercises  
- Educational demonstrations of AI vulnerabilities
- Improving AI safety measures

❌ **Inappropriate Use:**
- Attacking AI systems without authorization
- Generating content that violates terms of service
- Malicious exploitation of AI vulnerabilities
- Any illegal or harmful activities

## 🤝 Contributing

**We need your expertise!** This experimental V0.1 needs validation and improvement:

- **Security researchers** - test patterns against real systems and share results
- **AI safety experts** - improve primitive effectiveness and coverage  
- **Developers** - enhance the TypeScript implementation and API design
- **Feedback** - what works? what doesn't? what's missing?

See our [Design Documentation](./docs/design.md) for technical details on architecture and adding new attack primitives.

**Built with Claude Code** - This library was collaboratively designed and implemented using Claude Code, demonstrating AI-assisted security tool development.

## 📄 License

MIT License - See LICENSE for details.

## 🔗 Links

- **Documentation**: [Technical Design](./docs/design.md) | [API Reference](./docs/api.md)
- **Issues**: [Report bugs or request features](https://github.com/BlueprintLabIO/prompt-injector/issues)
- **Research**: Attack patterns based on published security research

---

**⚠️ Disclaimer**: Experimental software for authorized testing only. Use responsibly. Test only on AI systems you own or have explicit permission to test. Follow responsible disclosure practices and applicable laws. Success rates and effectiveness claims are based on preliminary research and may not reflect real-world performance.