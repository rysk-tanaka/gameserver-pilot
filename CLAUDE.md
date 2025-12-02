# CLAUDE.md - AI Assistant Guide for gameserver-pilot

This document provides comprehensive guidance for AI assistants working with the gameserver-pilot repository.

## Project Overview

**gameserver-pilot** is a game server project currently in its initial development phase. This repository serves as the foundation for building scalable, real-time game server infrastructure.

## Repository Status

This is a newly initialized repository. The codebase structure and conventions documented below represent the intended architecture and should be updated as the project evolves.

## Codebase Structure (Planned)

```
gameserver-pilot/
├── src/                    # Source code
│   ├── server/             # Server-side game logic
│   ├── networking/         # Network protocols and handlers
│   ├── game/               # Game state and mechanics
│   ├── utils/              # Utility functions
│   └── config/             # Configuration management
├── tests/                  # Test suites
│   ├── unit/               # Unit tests
│   ├── integration/        # Integration tests
│   └── load/               # Load/stress tests
├── docs/                   # Documentation
├── scripts/                # Build and deployment scripts
├── config/                 # Configuration files
└── docker/                 # Container definitions
```

## Development Workflow

### Getting Started

1. Clone the repository
2. Install dependencies (once package management is set up)
3. Configure environment variables
4. Run the development server

### Branch Naming Conventions

- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/*` - New features
- `fix/*` - Bug fixes
- `claude/*` - AI-assisted development branches

### Commit Message Format

Use clear, descriptive commit messages:
```
<type>: <short description>

[optional body with more details]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

## Key Conventions

### Code Style

- Use consistent formatting (configure linter/formatter once tech stack is chosen)
- Write self-documenting code with clear variable and function names
- Add comments only where logic isn't self-evident
- Keep functions focused and concise

### Architecture Principles

1. **Modularity**: Keep components loosely coupled
2. **Scalability**: Design for horizontal scaling from the start
3. **Real-time Performance**: Optimize for low latency
4. **State Management**: Clear separation of game state and network state
5. **Security**: Validate all client inputs, never trust the client

### Game Server Specifics

- **Tick Rate**: Define consistent server tick rate for game loop
- **State Synchronization**: Implement efficient delta compression
- **Connection Handling**: Graceful handling of disconnects/reconnects
- **Matchmaking**: Consider lobby and matchmaking patterns
- **Persistence**: Plan for game state persistence where needed

## Testing Strategy

### Test Categories

1. **Unit Tests**: Test individual functions and components
2. **Integration Tests**: Test component interactions
3. **Load Tests**: Verify performance under concurrent connections
4. **Network Tests**: Simulate various network conditions

### Running Tests

```bash
# Commands will be updated once test framework is configured
# npm test / cargo test / go test / etc.
```

## AI Assistant Guidelines

### When Working on This Repository

1. **Read before modifying**: Always read existing code before making changes
2. **Maintain consistency**: Follow established patterns and conventions
3. **Keep it simple**: Avoid over-engineering; solve the current problem
4. **Security-first**: Be vigilant about input validation and security
5. **Performance-aware**: Game servers are latency-sensitive

### Common Tasks

- **Adding a new feature**: Create in appropriate `src/` subdirectory
- **Fixing bugs**: Include test case that reproduces the issue
- **Refactoring**: Ensure tests pass before and after changes
- **Documentation**: Update relevant docs when changing behavior

### What to Avoid

- Don't add unnecessary dependencies
- Don't introduce breaking changes without discussion
- Don't commit sensitive data (API keys, credentials)
- Don't ignore error handling
- Don't skip input validation for network messages

## Environment Configuration

### Environment Variables (Planned)

```
SERVER_PORT=8080          # Main server port
TICK_RATE=60              # Server tick rate (Hz)
MAX_PLAYERS=100           # Maximum concurrent players
LOG_LEVEL=info            # Logging verbosity
```

## Dependencies

*To be populated once technology stack is chosen*

Common considerations for game servers:
- Networking library (WebSocket, TCP/UDP handling)
- Serialization (MessagePack, Protocol Buffers, etc.)
- Logging framework
- Metrics/monitoring
- Database driver (if persistence needed)

## Deployment

### Local Development

```bash
# Setup commands will be added once project structure is established
```

### Production Deployment

*Deployment procedures to be documented as infrastructure is set up*

Considerations:
- Container orchestration (Kubernetes, Docker Swarm)
- Load balancing
- Health checks
- Graceful shutdown
- Scaling policies

## Monitoring and Observability

### Metrics to Track

- Active connections
- Messages per second
- Tick processing time
- Memory usage
- Network bandwidth
- Error rates

### Logging Standards

- Use structured logging (JSON format)
- Include correlation IDs for request tracing
- Log at appropriate levels (debug, info, warn, error)

## Contributing

1. Create a feature branch from `develop`
2. Make changes following the conventions above
3. Ensure all tests pass
4. Submit a pull request with clear description
5. Address review feedback

## Maintenance Notes

### Updating This Document

Update CLAUDE.md when:
- Adding new directories or major components
- Changing development workflows
- Adding new conventions or patterns
- Updating dependencies or tooling
- Changing deployment procedures

---

*Last updated: 2025-12-02*
*Repository status: Initial setup phase*
