# SOFTWARE REQUIREMENTS SPECIFICATION (SRS)

## DSA Mentor — Personalized Agentic RAG Platform

Version: 1.0

---

## 1. Introduction

### 1.1 Purpose

The purpose of this Software Requirements Specification (SRS) is to define the functional and non-functional requirements of DSA Mentor — Personalized Agentic RAG Platform.

The system is an AI-powered learning assistant designed to help students prepare for Data Structures and Algorithms (DSA). It uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from a curated DSA knowledge base and provide accurate, context-aware responses.

Unlike a traditional chatbot, the system is designed to support multiple DSA learning activities such as concept explanation, problem pattern identification, progressive hint generation, similar problem recommendations, solution explanation, complexity analysis, and personalized practice recommendations.

The platform will use advanced retrieval techniques such as hybrid search, metadata filtering, query rewriting, reranking, and contextual compression. An agentic workflow will be used to route user requests to appropriate components and perform multi-step retrieval when required.

### 1.2 Scope

The DSA Mentor platform will provide an intelligent environment for DSA preparation using a curated knowledge base containing DSA concepts, algorithms, problem descriptions, patterns, approaches, solutions, complexity analysis, common mistakes, and related problems.

The system will allow users to:

- Ask questions about DSA concepts and algorithms.
- Search for relevant DSA problems.
- Identify the likely pattern required to solve a problem.
- Receive progressive hints instead of immediately receiving complete solutions.
- Understand approaches and optimal solutions.
- Find similar problems based on concepts and patterns.
- Analyze time and space complexity.
- Maintain and analyze problem-solving progress.
- Receive personalized practice recommendations.
- Interact with an AI-based DSA mentor through a conversational interface.
- Receive responses grounded in the project's curated knowledge base with relevant source references.

The project will combine RAG, agentic workflows, vector search, keyword search, metadata filtering, and structured user-progress data.

### 1.3 Definitions, Acronyms and Abbreviations

| Term | Definition |
| --- | --- |
| DSA | Data Structures and Algorithms |
| RAG | Retrieval-Augmented Generation |
| LLM | Large Language Model |
| API | Application Programming Interface |
| UI | User Interface |
| DB | Database |
| Vector Database | Database used to store and search vector embeddings |
| Embedding | Numerical representation of text used for semantic similarity search |
| Hybrid Search | Combination of semantic/vector search and keyword-based search |
| Reranking | Reordering retrieved results according to relevance |
| Metadata | Structured information associated with a document or problem |
| Agentic RAG | RAG architecture where an AI agent dynamically selects actions and retrieval strategies |
| RBAC | Role-Based Access Control |

### 1.4 Intended Users

The primary users of the system are:

1. Students preparing for coding interviews and technical examinations.
2. DSA learners who want concept explanations and guided practice.
3. Competitive programmers seeking pattern-based problem recommendations.
4. Administrators responsible for managing the DSA knowledge base.

---

## 2. Overall Description

### 2.1 Product Perspective

DSA Mentor is a web-based AI learning platform consisting of a frontend application, backend API, RAG pipeline, AI agent, vector database, and relational database.

The overall architecture is:

```text
User
  ↓
React Frontend
  ↓
FastAPI Backend
  ↓
Query Router / Agent
  ↓
────────────────────────────────────
Concept Query     Problem Query     Progress Query
     ↓                 ↓                 ↓
 RAG Pipeline      RAG Pipeline       PostgreSQL
     ↓                 ↓                 ↓
────────────────────────────────────
              Response Generator
                    ↓
                   User
```

The RAG pipeline will retrieve information from a curated DSA knowledge base.

The knowledge base may contain information related to:

- Arrays
- Strings
- Hashing
- Linked Lists
- Stacks
- Queues
- Recursion
- Backtracking
- Binary Search
- Trees
- Binary Search Trees
- Heaps
- Graphs
- Greedy Algorithms
- Dynamic Programming
- Tries
- Bit Manipulation
- Advanced Algorithms

### 2.2 Product Functions

The major functions of the system include:

1. User Authentication

The system shall allow users to register, log in, and manage their accounts.

2. Concept Learning

The system shall answer questions related to DSA concepts and algorithms.

3. Problem Analysis

The system shall analyze a problem statement and identify relevant topics and possible patterns.

4. Progressive Hint Generation

The system shall provide hints in multiple levels without immediately revealing the complete solution.

5. Pattern Identification

The system shall identify possible DSA patterns, such as:

- Sliding Window
- Two Pointers
- Binary Search
- Prefix Sum
- Hashing
- Recursion
- Backtracking
- BFS
- DFS
- Dynamic Programming
- Greedy
- Monotonic Stack
- Heap/Priority Queue

6. Similar Problem Recommendation

The system shall retrieve and recommend problems related to the user's current problem or selected topic.

7. Solution Explanation

The system shall explain the intuition, algorithm, implementation approach, and complexity of a solution.

8. Personalized Progress Tracking

The system shall store information about solved problems and topic-wise progress.

9. Personalized Recommendations

The system shall recommend problems based on user performance, solved problems, and weak areas.

10. Knowledge Base Retrieval

The system shall retrieve relevant information using semantic and keyword-based search.

11. Source-Aware Responses

The system shall provide relevant problem or knowledge-base references used to generate the response where applicable.

12. Administration

Administrators shall be able to add, update, or remove DSA knowledge-base content.

---

## 3. Functional Requirements

### FR-01: User Registration

The system shall allow a new user to create an account using valid registration details.

The system shall:

- Validate user input.
- Prevent duplicate accounts.
- Securely store user credentials.
- Create a unique user account.

### FR-02: User Login

The system shall allow registered users to log in securely.

Upon successful authentication, the system shall provide access to authorized features.

### FR-03: DSA Concept Query

The system shall allow users to ask questions related to DSA concepts.

Example queries include:

- What is a sliding window?
- When should binary search be used?
- Explain memoization and tabulation.
- What is the difference between BFS and DFS?

The system shall retrieve relevant knowledge-base content and generate a context-aware answer.

### FR-04: Problem Pattern Identification

The system shall allow users to submit a problem statement.

The system shall analyze the problem and identify:

- Relevant topic.
- Possible DSA pattern.
- Important constraints.
- Key observations.
- Related problems.

The response shall explain why a particular pattern is suitable.

### FR-05: Progressive Hint Generation

The system shall provide hints in multiple levels.

The default sequence shall be:

Level 1: General observation

Level 2: Direction toward the appropriate data structure or algorithm

Level 3: Core approach

Level 4: Step-by-step algorithm

Level 5: Complete solution

The system shall avoid revealing later hint levels unless requested by the user.

### FR-06: Similar Problem Recommendation

The system shall recommend problems similar to the user's current query or problem.

Similarity may be determined using:

- DSA topic.
- Algorithmic pattern.
- Semantic similarity.
- Difficulty level.
- Related concepts.

The system shall return relevant problem recommendations with available metadata.

### FR-07: Solution Explanation

The system shall provide explanations for DSA solutions.

The explanation may include:

1. Problem intuition.
2. Brute-force approach where relevant.
3. Optimized approach.
4. Step-by-step algorithm.
5. Time complexity.
6. Space complexity.
7. Common mistakes.
8. Related patterns.

The system shall support Java as the primary programming language for code explanations.

### FR-08: Query Rewriting

The system shall improve ambiguous or context-dependent user queries before retrieval.

For example:

Original Query:
"What about its complexity?"

Based on previous conversation context:

Rewritten Query:
"What is the time and space complexity of the sliding window approach?"

The rewritten query shall be used to improve retrieval quality.

### FR-09: Hybrid Retrieval

The system shall support hybrid search by combining:

- Vector-based semantic search.
- Keyword-based search.

The system shall combine the results and return relevant candidate documents.

### FR-10: Metadata Filtering

The system shall filter retrieval results using metadata.

Supported metadata may include:

- Topic.
- Subtopic.
- Pattern.
- Difficulty.
- Problem ID.
- Programming language.
- Content type.

Example:

A user requesting "medium dynamic programming problems" may be filtered using:

Topic = Dynamic Programming
Difficulty = Medium

### FR-11: Reranking

The system shall rerank retrieved results according to their relevance to the user's query.

The system shall select the most relevant results before generating the final response.

### FR-12: Contextual Compression

The system shall reduce irrelevant information from retrieved documents before passing context to the language model when required.

The purpose shall be to:

- Reduce unnecessary context.
- Improve response relevance.
- Reduce token usage.
- Improve generation efficiency.

### FR-13: Parent Document Retrieval

The system shall support parent-child document relationships where applicable.

Small child chunks shall be used for precise retrieval, while larger parent sections may be retrieved to provide additional context.

### FR-14: Agentic Query Routing

The system shall classify incoming requests and route them to an appropriate workflow.

Possible request categories include:

- Concept explanation.
- Problem analysis.
- Hint generation.
- Similar problem search.
- Solution explanation.
- Progress analysis.
- Practice planning.

The AI agent shall select the required retrieval source or tool based on the request.

### FR-15: User Progress Tracking

The system shall allow users to maintain information regarding solved problems.

Stored information may include:

- Problem identifier.
- Problem name.
- Topic.
- Difficulty.
- Status.
- Date solved.
- Number of attempts.

### FR-16: Weak Area Analysis

The system shall analyze user progress and identify potential weak topics.

The analysis may consider:

- Number of solved problems.
- Topic-wise distribution.
- Difficulty distribution.
- Attempt history.
- Unsolved or repeatedly attempted problems.

The system shall generate personalized observations and recommendations.

### FR-17: Personalized Practice Plan

The system shall generate a practice plan based on user progress and preferences.

The user may specify:

- Available preparation time.
- Target difficulty.
- Topics to focus on.
- Number of problems.

The system shall recommend relevant topics and problems.

### FR-18: RAG Evaluation

The system shall support evaluation of the RAG pipeline using a predefined evaluation dataset.

Evaluation metrics may include:

- Context precision.
- Context recall.
- Faithfulness.
- Answer relevance.
- Answer correctness.

Evaluation results shall be used to identify weaknesses in the retrieval and generation pipeline.

### FR-19: Knowledge Base Management

The administrator shall be able to:

- Add DSA documents.
- Add problem information.
- Update existing knowledge.
- Delete obsolete content.
- Assign metadata.
- Trigger indexing and embedding generation.

---

## 4. Non-Functional Requirements

### NFR-01: Performance

The system should provide responses within an acceptable time under normal operating conditions.

The system should optimize latency using techniques such as:

- Caching.
- Asynchronous processing.
- Parallel retrieval where applicable.
- Efficient database queries.
- Controlled retrieval size.

### NFR-02: Scalability

The backend shall be designed to support increasing numbers of users.

The application should support horizontal scaling of stateless services where required.

### NFR-03: Reliability

The system shall handle failures gracefully.

The backend should implement appropriate mechanisms for:

- API timeouts.
- Retry handling.
- External service failures.
- Database connection failures.
- Rate-limit handling.

### NFR-04: Security

The system shall protect user data and credentials.

Security requirements include:

- Secure password storage.
- Authenticated API access.
- Authorization checks.
- Input validation.
- Protection of sensitive configuration values.
- Secure storage of API keys through environment variables.

### NFR-05: Usability

The application shall provide a simple and intuitive interface.

Users shall be able to:

- Ask questions easily.
- Select learning modes.
- Request additional hints.
- View retrieved sources.
- Track progress.
- View recommendations.

### NFR-06: Maintainability

The system shall use a modular architecture.

Major components shall be separated into modules such as:

- Authentication.
- Knowledge ingestion.
- Retrieval.
- Reranking.
- Agent workflow.
- Progress tracking.
- Recommendation.
- Evaluation.

### NFR-07: Availability

The deployed application should be designed to remain available under normal operating conditions.

Appropriate monitoring and error logging should be implemented to detect failures.

### NFR-08: Observability

The system should record relevant operational information, including:

- Request latency.
- Retrieval latency.
- LLM latency.
- Errors.
- Retrieved document information.
- Token usage where available.
- Evaluation results.

---

## 5. System Architecture

The proposed architecture is:

```text
                         USER
                           │
                           ▼
                    React Frontend
                           │
                           ▼
                     FastAPI Backend
                           │
                           ▼
                    Authentication
                           │
                           ▼
                    Agent / Router
                           │
          ┌────────────────┼─────────────────┐
          │                │                 │
          ▼                ▼                 ▼
    Concept RAG       Problem RAG      Progress Tool
          │                │                 │
          └────────────────┼─────────────────┘
                           │
                           ▼
                    Query Rewriting
                           │
                           ▼
                   Metadata Filtering
                           │
                           ▼
                     Hybrid Search
                    ┌──────┴──────┐
                    ▼             ▼
              Vector Search       BM25
                    └──────┬──────┘
                           ▼
                       Reranking
                           │
                           ▼
                 Contextual Compression
                           │
                           ▼
                          LLM
                           │
                           ▼
                    Final Response
                           │
                           ▼
                         USER
```

---

## 6. Data Requirements

### 6.1 DSA Knowledge Base

Each DSA problem or concept may contain the following fields:

- ID
- Title
- Content Type
- Topic
- Subtopic
- Pattern
- Difficulty
- Problem Statement
- Constraints
- Key Observations
- Intuition
- Approach
- Algorithm
- Java Solution
- Time Complexity
- Space Complexity
- Common Mistakes
- Related Problems
- Source Reference

### 6.2 User Data

The system may store:

- User ID
- Username
- Email
- Password Hash
- Account Creation Date

### 6.3 Progress Data

The system may store:

- Progress ID
- User ID
- Problem ID
- Topic
- Difficulty
- Status
- Attempts
- Date Started
- Date Solved

---

## 7. External Interface Requirements

### 7.1 User Interface

The frontend shall contain the following major screens:

#### Authentication Page

- Register.
- Login.

#### Chat/Assistant Page

- User query input.
- AI response.
- Source references.
- Hint controls.
- Learning mode selection.

#### Problem Analysis Page

- Problem input.
- Pattern analysis.
- Suggested approach.
- Related problems.

#### Progress Dashboard

- Topic-wise progress.
- Difficulty-wise distribution.
- Weak areas.
- Recommendations.

#### Admin Panel

- Knowledge-base management.
- Document upload.
- Metadata management.
- Indexing controls.

### 7.2 API Interface

The backend shall expose APIs for:

- POST /auth/register
- POST /auth/login
- POST /chat
- POST /problems/analyze
- POST /problems/hint
- GET /problems/similar
- POST /progress
- GET /progress
- GET /recommendations
- POST /admin/documents
- POST /admin/index

The final API design may be modified during implementation.

---

## 8. Technology Stack

| Layer | Technology |
| --- | --- |
| Frontend | React |
| Backend | FastAPI |
| RAG Framework | LangChain |
| Agent Workflow | LangGraph |
| Vector Database | Qdrant |
| Relational Database | PostgreSQL |
| Cache | Redis |
| Keyword Retrieval | BM25 |
| Embeddings | Sentence Transformers or API-based embeddings |
| LLM | Configurable LLM Provider |
| Containerization | Docker |
| Evaluation | RAG evaluation framework / LLM-as-a-Judge |
| Deployment | Cloud-based deployment platform |

---

## 9. Constraints

The system will operate under the following constraints:

1. Answer quality depends on the quality and coverage of the curated DSA knowledge base.
2. External LLM services may have API rate limits and usage costs.
3. Retrieval quality may vary depending on chunking, embedding models, and query complexity.
4. Some advanced RAG components may increase latency and computational cost.
5. The system shall prioritize educational assistance and should encourage users to attempt problems before revealing complete solutions.
6. The first version of the project may support a limited number of topics and problems.

---

## 10. Future Enhancements

Future versions may include:

- Voice-based interaction.
- Code execution and test-case evaluation.
- Automatic code debugging.
- LeetCode or other platform progress integration where officially supported.
- Mock technical interviews.
- Adaptive difficulty selection.
- Spaced-repetition-based revision.
- Contest preparation mode.
- Multi-language code support.
- Collaborative learning.
- Advanced analytics dashboard.
- Fine-tuned recommendation models.

---

## 11. Acceptance Criteria

The project shall be considered functionally successful when:

1. Users can register and log in.
2. Users can ask DSA-related questions and receive relevant responses.
3. The system can retrieve information from the DSA knowledge base.
4. The system can identify relevant DSA patterns for supported problem queries.
5. Users can receive progressive hints.
6. The system can recommend similar problems.
7. User progress can be stored and retrieved.
8. The system can identify topic-wise learning gaps using available progress data.
9. The agent can route supported requests to the appropriate workflow.
10. Retrieval and answer quality can be evaluated using a defined evaluation dataset.
11. The application can be deployed and accessed through a web interface.

---

## 12. Conclusion

DSA Mentor is an AI-powered learning platform designed to provide personalized and context-aware assistance for Data Structures and Algorithms preparation. The system combines Retrieval-Augmented Generation with advanced retrieval techniques and agentic workflows to go beyond a traditional PDF chatbot.

The platform focuses on helping users understand concepts, identify patterns, receive progressive hints, discover related problems, and track their preparation progress. The use of hybrid retrieval, metadata filtering, query rewriting, reranking, contextual compression, and RAG evaluation is intended to improve the relevance and quality of responses.

The proposed system is designed as a modular and scalable project that can initially be implemented as a DSA RAG assistant and gradually extended into a production-oriented personalized AI mentor.

---

# AlgoMentor — Personalized Agentic RAG Platform for DSA Preparation
