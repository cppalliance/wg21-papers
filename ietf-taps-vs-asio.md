|   |   |
|---|---|
| Document:   | DXXXX
| Date:       | 2025-12-30
| Reply-to:   | Vinnie Falco \<vinnie.falco@gmail.com\>
| Audience:   | SG1, LEWG

---

# IETF TAPS versus Boost.Asio: Top-Down Design versus Use-Case-First Design

**Abstract**

The history of networking standards is littered with elegant abstractions that failed to achieve adoption. The OSI seven-layer model stands as the canonical example: a comprehensive framework that lost to TCP/IP's pragmatic design. This paper examines the IETF Transport Services (TAPS) initiative and compares it to Boost.Asio, arguing that TAPS exhibits the same "framework-first" design pathology that doomed OSI protocols. While TAPS offers a theoretically appealing abstraction over transport protocols, its lack of real-world deployment after a decade of development—contrasted with Boost.Asio's twenty-plus years of production use—suggests that C++ standardization efforts should prioritize proven practice over speculative architecture.

---

## 1. Introduction

In 2014, the C++ committee made a decision to "adopt existing practice" for a standard networking proposal, specifically adopting a proposal based on the widely-used Asio library. The resulting Networking TS represented years of effort to codify patterns proven across millions of deployed applications.

A decade later, WG21's SG4 networking study group is considering an alternative direction: basing C++ standard networking on the IETF's Transport Services Application Programming Interface (TAPS). Papers P3185 and P3482 propose aligning C++ networking with this IETF initiative, arguing that TAPS represents "the industry expert's current thinking" on networking API design.

This paper examines whether TAPS actually represents industry practice or whether it represents the opposite—an academic framework developed in isolation from real-world deployment, much like the OSI protocols that preceded TCP/IP's dominance.

## 2. The OSI Precedent: Framework-First Design

### 2.1 The Promise of OSI

The Open Systems Interconnection model promised a comprehensive, layered approach to networking. Its seven layers—Physical, Data Link, Network, Transport, Session, Presentation, and Application—offered clean separation of concerns and protocol independence. Standards bodies invested enormous effort in developing OSI protocols to instantiate this model.

### 2.2 The Reality

OSI protocols failed catastrophically in the marketplace. Several factors contributed:

**Bad Timing**: By the time OSI specifications were finalized, TCP/IP had already achieved critical mass. Companies had invested in TCP/IP implementations, and the switching costs to OSI were prohibitive.

**Bad Technology**: The OSI model's upper layers (5-6) never mapped to reality. The Session Layer's "synchronization points" proved impractical—modern distributed synchronization, exemplified by Google's Paxos implementation, is far more complex than any standardizable layer could accommodate. The Presentation Layer's vision of universal data format translation similarly failed to materialize.

**Bad Implementations**: Initial OSI implementations were slow and unwieldy. The specification's complexity led directly to implementation complexity, and "OSI became synonymous with poor quality in early days."

**Disconnection from Practice**: OSI was developed through a standards-first process that prioritized theoretical elegance over running code. The IETF's principle of "rough consensus and running code" emerged partly as a reaction to OSI's failures.

### 2.3 The Lesson

The OSI model survives as a pedagogical tool—useful for explaining networking concepts—but the protocols designed to instantiate it are largely forgotten. TCP/IP's pragmatic, use-case-driven design won because it solved real problems that real programmers had, even if its architecture was less theoretically satisfying.

## 3. IETF TAPS: Architecture and Ambitions

### 3.1 What TAPS Proposes

TAPS is an IETF Standards Track initiative to define a language-agnostic abstract architecture for exposing transport protocol features to applications. The initiative comprises three main documents:

- **draft-ietf-taps-arch**: The architectural framework
- **draft-ietf-taps-interface**: The abstract API specification
- **draft-ietf-taps-impl**: Implementation guidance

TAPS aims to "replace the BSD sockets API as the common interface to the transport layer." Rather than applications binding directly to TCP or UDP, they would specify abstract requirements—reliability, ordering, latency constraints—and the transport system would select appropriate protocols at runtime.

### 3.2 The TAPS Vision

The TAPS architecture promises several benefits:

**Protocol Agility**: Applications specify *what* they need, not *how* to achieve it. The transport system can select TCP, SCTP, QUIC, or future protocols without application changes.

**Connection Racing**: TAPS implementations can race multiple protocol candidates in parallel, selecting the first successful connection.

**Message Orientation**: Unlike BSD sockets' stream abstraction for TCP, TAPS presents all communication as message-oriented, with application-assisted framing where needed.

**Secure by Default**: TAPS integrates transport security as a first-class concern rather than a bolted-on layer.

### 3.3 The TAPS Working Group Status

The TAPS working group was chartered in 2014. As of late 2024, its core documents remain Internet-Drafts (draft-26 of the interface specification). The working group's charter page notes:

> "TAPS has delivered all the deliverables it was chartered for... With a hope that TAPS will be deployed gradually."

This phrasing—"with a hope"—is revealing. After a decade of work, widespread deployment remains aspirational.

## 4. TAPS Implementations: The Deployment Gap

### 4.1 Apple's Network.framework

Apple's Network.framework, introduced in iOS 12 and macOS 10.14 (2018), is described as "a nearly-compliant implementation" of TAPS that "will slowly converge with TAPS after publication."

This represents the only production-grade TAPS implementation. Notably:

- It is proprietary and platform-specific
- It predates TAPS standardization, meaning TAPS was arguably influenced by Network.framework rather than the reverse
- Apple has not publicly committed to full TAPS compliance

### 4.2 NEAT: The EU Research Project

The NEAT (New, Evolutive API and Transport-Layer Architecture for the Internet) project was funded by the European Union's Horizon 2020 program. It produced the first open-source TAPS implementation in C.

NEAT's trajectory is instructive:

- Active development: 2015-2018
- Project ended: February 2018 (when EU funding concluded)
- Current status: Abandoned

The NEAT GitHub repository shows the last commit to core functionality in 2018. The project website's final blog posts describe a "farewell IETF meeting" and optimistic hopes for continued TAPS standardization work.

### 4.3 Other Implementations

- **NEATPy**: A Python wrapper around NEAT, development ceased mid-2020
- **python-asyncio-taps**: An academic implementation against an early draft (draft-04), not actively maintained
- **PyTAPS**: Referenced in IETF mailing lists, limited deployment evidence

### 4.4 Summary of Field Experience

| Implementation | Platform | Status | Production Use |
|---------------|----------|--------|----------------|
| Network.framework | Apple only | Active | Yes (Apple ecosystem) |
| NEAT | Linux/BSD | Abandoned 2018 | Research only |
| NEATPy | Python | Abandoned 2020 | None known |
| python-asyncio-taps | Python | Stale | None known |

The P3482 WG21 paper acknowledges this reality: "Unfortunately, at present, Apple's Network Framework is the only such implementation."

## 5. Boost.Asio: Use-Case-First Design

### 5.1 Design Philosophy

Boost.Asio's documented design goals stand in stark contrast to TAPS:

> "Model concepts from established APIs, such as BSD sockets. The BSD socket API is widely implemented and understood, and is covered in much literature. Other programming languages often use a similar interface for networking APIs. As far as is reasonable, Boost.Asio should leverage existing practice."

This is explicitly a use-case-first philosophy: start with what programmers already know and need, then provide abstractions that make common tasks easier without obscuring the underlying model.

### 5.2 Architectural Approach

Asio provides:

**Proactor Pattern**: Asynchronous operations that notify completion rather than blocking. On platforms with native async I/O (Windows IOCP), Asio uses it directly. On others (Linux epoll, BSD kqueue), it implements the proactor pattern atop reactor primitives.

**Executor Model**: Explicit control over where and how completion handlers execute, enabling sophisticated concurrency patterns without hidden threading.

**Composition**: Operations compose through completion tokens, allowing the same async operations to integrate with callbacks, futures, coroutines, or custom mechanisms.

**Direct Protocol Access**: TCP, UDP, and other protocols are directly accessible. Programmers understand exactly what protocol they're using.

### 5.3 Deployment Evidence

Asio's deployment is extensive:

- **Boost.Beast**: High-performance HTTP and WebSocket implementation
- **libpion**: Embedded HTTP server
- **cpp-netlib**: Network library collection
- **Countless proprietary applications**: Financial trading systems, game servers, IoT platforms

The library has been in active development and production use since 2003—over twenty years of continuous field experience across every major platform.

### 5.4 Evolution Through Practice

Asio has evolved based on real-world feedback:

- Executor model refined through years of use
- Completion token mechanism generalized from experience with different async patterns
- SSL/TLS integration developed in response to actual security requirements
- Coroutine support added as C++20 coroutines emerged

Each evolution addressed concrete problems encountered by actual users rather than theoretical concerns identified by committee.

## 6. Comparative Analysis

### 6.1 Abstraction Level

**TAPS**: Abstracts away protocol selection entirely. Applications specify properties; the system chooses protocols.

**Asio**: Provides protocol-specific types (`tcp::socket`, `udp::socket`) while abstracting platform differences.

The TAPS approach assumes protocol agility is a common need. In practice, most applications have specific protocol requirements dictated by their domain: a web server needs HTTP/HTTPS over TCP; a DNS resolver needs UDP with TCP fallback; a game server may need UDP with custom reliability. The cases where "any reliable transport" suffices are rarer than TAPS's design assumes.

### 6.2 Complexity

**TAPS**: The interface specification alone runs to 26 drafts over a decade. Concepts include Preconnections, Connection Groups, Selection Properties, Connection Properties, Message Properties, Framers, and Racing.

**Asio**: Core concepts are `io_context`, sockets, buffers, and completion handlers. Additional complexity (`strand`, timers, SSL) is additive and optional.

TAPS's complexity serves its abstraction goals but imposes costs on every user, whether or not they need protocol agility. Asio's complexity is pay-as-you-go: simple programs remain simple.

### 6.3 Secure-by-Default

Both TAPS proponents and Asio critics note that Asio does not enforce secure connections by default. This is a legitimate concern that the P1860/P1861 papers address.

However, this is an orthogonal issue. Asio could be extended to default to TLS without adopting TAPS's full abstraction model. The secure-by-default requirement does not necessitate protocol abstraction.

### 6.4 Implementation Burden

**TAPS**: Requires implementing protocol racing, property-based selection, connection caching, multipath support, and automatic fallback. The implementation guidance document runs to hundreds of pages.

**Asio**: Wraps platform-native async I/O primitives. Core functionality maps directly to OS capabilities.

Standard library implementers—already stretched thin—face a dramatically higher burden with TAPS. The P3185 paper asks: "Can the stdlib implementers adopt a proposal of this complexity?" The honest answer, given NEAT's abandonment when EU funding ended, is uncertain at best.

### 6.5 The Maturity Critique

Some WG21 participants and vocal members of the C++ community dismiss Asio as "outdated." This critique inverts the correct inference.

A library that has survived twenty years of production use, adapted to four major C++ standard revisions (C++11 move semantics, C++14/17 refinements, C++20 coroutines), and spawned successful derivative works is not outdated—it is validated. The distinction matters:

- **"Old" versus "Outdated"**: TCP/IP is older than OSI. BSD sockets are older than every proposed replacement. Age combined with continued use equals validation. Age combined with abandonment equals obsolescence. Asio is emphatically the former.

- **The Lindy Effect**: Systems that have survived twenty years of production use are statistically more likely to survive the next twenty than systems with no deployment history. TAPS's novelty is a liability, not an asset.

- **Living Tradition**: Asio's continuous evolution—executor model refinement, completion token generalization, coroutine integration—demonstrates a living tradition of knowledge. A truly outdated library would have been abandoned, not continuously adapted.

The burden of proof lies with the replacement. What does TAPS offer that Asio cannot evolve to provide? If the answer is "protocol abstraction," the follow-up question is: who has demonstrated demand for this capability outside academic papers? If Asio is outdated, why does it continue to accumulate production deployments while TAPS accumulates draft revisions?

Maturity is not a defect to be overcome. It is evidence that a design has survived the harshest test: sustained use by programmers solving real problems.

## 7. The Standards Process Failure Mode

### 7.1 RFC 3774: IETF Problem Statement

The IETF itself has documented the pathology that TAPS exemplifies. RFC 3774 (2004) identified:

> "Implementation or deployment experience is still not required, so the IETF's guiding principle of 'rough consensus and running code' has less of a chance to be effective."

> "There appears to be a vicious circle in operation where vendors tend to deploy protocols that have reached [Proposed Standard] as if they were ready for full production, rather than accepting that standards at the PS level may require changes."

TAPS has been in development for over a decade without achieving even Proposed Standard status. The one significant implementation (Apple's) is proprietary and not fully compliant. The open-source implementation (NEAT) was abandoned when research funding ended.

### 7.2 The Deployment Test

The ultimate test of any API design is deployment. Standards that achieve deployment evolve based on implementation experience; standards that don't achieve deployment remain theoretical exercises.

BSD sockets, despite their warts, achieved universal deployment. Every operating system implements them. Every programmer knows them. Libraries like Asio build on this foundation rather than replacing it.

TAPS proposes to replace BSD sockets but has not achieved the deployment that would validate its design choices. Adopting TAPS for C++ standard networking would mean standardizing an API whose design assumptions remain largely untested in production.

## 8. An Institutional Analysis

The contrast between TAPS and Asio is not merely technical—it reflects deeper patterns in how institutions create and preserve knowledge. Great Founder Theory (GFT), a framework for analyzing institutional dynamics developed by Samo Burja, illuminates why framework-first standards consistently fail while practitioner-driven designs succeed.

### 8.1 Live Players and Dead Players

GFT distinguishes between **live players**—individuals or tightly coordinated groups capable of doing things they haven't done before—and **dead players** working from fixed scripts. This distinction maps precisely onto our comparison.

**Chris Kohlhoff and Asio** exhibit the hallmarks of a live player:
- Continuous adaptation to new requirements (C++11 move semantics, C++20 coroutines)
- Evolution into unexpected domains (the executor model influencing P2300)
- Responsiveness to user feedback across two decades
- Production of derivative works (Beast, libpion) that extend the original vision

**The TAPS Working Group** exhibits the hallmarks of a dead player:
- A decade of drafts following a predetermined specification process
- Inability to adapt when implementations (NEAT) failed
- No response mechanism to deployment feedback—because there is no deployment
- Aspirational language ("with a hope") substituting for demonstrated capability

The NEAT project's trajectory is particularly instructive. When EU Horizon 2020 funding ended in 2018, development ceased immediately. A live tradition of knowledge survives funding disruptions because practitioners are intrinsically motivated and possess transferable skills. NEAT's instant death reveals it was never a living tradition—merely a funded research project that produced papers rather than lasting capability.

### 8.2 Functional Institutions Are the Exception

GFT's central insight is that "functional institutions are the exception, not the rule." Most institutions inadequately imitate functional ones, copying external forms without understanding underlying mechanisms. They optimize for appearance rather than reality.

The OSI model exemplifies this pattern. Its seven-layer architecture looked comprehensive and professional. Standards bodies invested enormous resources. The external forms of success—committees, specifications, official status—were all present. But the protocols never achieved deployment because the institution producing them was optimizing for theoretical elegance rather than practical utility.

TAPS replicates this pattern:
- Extensive documentation (the appearance of thoroughness)
- IETF imprimatur (borrowed prestige from a functional institution)
- Abstract completeness (every transport feature catalogued)
- No sustained implementation (the absence of actual functionality)

Asio, by contrast, exhibits the signs of a functional institution:
- **Production of notable effects**: Millions of deployed applications
- **Shared methodology**: The proactor pattern, completion tokens
- **Master/apprentice relationships**: Kohlhoff's influence on subsequent library authors
- **Extension of theory**: Beast building HTTP/WebSocket atop Asio primitives

### 8.3 The Committee Problem

GFT observes that "contrarian ideas—as all new technologies are by definition—almost never survive committees." Committees create the illusion of avoiding risk while actually maximizing it through inaction and consensus-seeking.

This explains why standards bodies consistently produce framework-first designs:
- Frameworks appear comprehensive and defensible
- They satisfy diverse stakeholders by abstracting over differences
- They avoid controversial choices by deferring them to "implementation"
- They provide intellectual satisfaction without requiring deployment risk

BSD sockets succeeded not because a committee designed them, but because practitioners at Berkeley built what they needed. The API emerged from use, was refined through deployment, and achieved standardization only after proving itself. TAPS inverts this sequence: standardize first, hope for deployment later.

### 8.4 Social Technology and Knowledge Transfer

BSD sockets represent successful **social technology**—a coordination mechanism that "can be documented and taught." Every operating system implements them. Every networking textbook covers them. Every programmer learns them. This universality is not an accident; it reflects decades of accumulated practice, teaching, and refinement.

TAPS attempts to replace this social technology without the social infrastructure to support it. There is no ecosystem of TAPS tutorials, no generation of programmers trained in TAPS patterns, no body of production experience to draw upon. The knowledge exists only in specification documents—what GFT calls a "dead tradition" where "external forms have been transferred, but not the full understanding of how to carry out this tradition as practiced."

The IETF's own principle of "rough consensus and running code" emerged as social technology specifically because OSI failed. Yet TAPS violates this principle: after a decade, there is neither rough consensus (only one partial implementation exists) nor running code (NEAT is abandoned, Apple's is proprietary and non-compliant).

### 8.5 The Succession Problem

Functional institutions must solve **the succession problem**: transferring both power and skill to maintain institutional health across generations. Asio has solved this repeatedly:
- The executor model evolved through multiple contributors
- Beast demonstrates successful knowledge transfer (Vinnie Falco built on Kohlhoff's foundation)
- The Networking TS process involved multiple implementers

TAPS has no succession problem because there is nothing to succeed. No living tradition exists to transfer. When NEAT's researchers moved on, the knowledge died with the funding. This is the signature of a non-functional institution: it cannot reproduce itself.

### 8.6 Implications for WG21

GFT suggests that WG21 faces a choice between two institutional patterns:

**Pattern A (Framework-First)**: Adopt TAPS, creating a standard that exists primarily in specification documents, hoping implementations will follow. This is the OSI pattern—comprehensive, theoretically elegant, and historically unsuccessful.

**Pattern B (Practice-First)**: Extend Asio, building on two decades of production experience, addressing specific deficiencies (security, sender/receiver integration) through targeted evolution. This is the TCP/IP pattern—pragmatic, incrementally refined, and historically successful.

The historical record strongly favors Pattern B. Functional institutions arise from founders who know how to coordinate people toward practical goals, not from committees optimizing for theoretical completeness.

## 9. Recommendations for WG21

### 9.1 Prioritize Proven Practice

The 2014 decision to adopt existing practice for C++ networking was correct. Asio represents two decades of field experience, continuous evolution based on user feedback, and deployment across countless production systems.

The Networking TS's issues—lack of secure-by-default, async model incompatibility with P2300—are real but addressable within the existing architectural framework. P2762 demonstrates that sender/receiver integration is achievable without abandoning the socket-based model.

### 9.2 Treat TAPS as Informational

TAPS documents contain useful analysis of transport protocol capabilities. The working group's survey of transport features (RFC 8095, RFC 8922, RFC 8923) provides valuable reference material.

However, informational value differs from prescriptive API design. TAPS's abstract API should inform C++ networking design, not dictate it.

### 9.3 Require Implementation Experience

Any significant API proposal should demonstrate implementation viability through:

- At least two independent implementations
- Production deployment evidence
- Multi-year stability in the face of real-world requirements

TAPS fails all three criteria outside Apple's proprietary ecosystem.

### 9.4 Address Security Separately

The secure-by-default concern is legitimate and should be addressed. However, security policy can be layered atop existing socket abstractions without requiring TAPS's full protocol abstraction model. Asio's SSL support demonstrates this approach.

## 10. Conclusion

The OSI model taught the networking community that theoretical elegance does not guarantee practical success. Protocols succeed through deployment, iteration, and responsiveness to real-world needs—not through comprehensive up-front specification. Great Founder Theory explains *why*: functional institutions are the exception, arising from founders who build living traditions of knowledge through practice, not committees that optimize for theoretical completeness.

IETF TAPS exhibits the hallmarks of a non-functional institution:

- A decade of specification work without sustained implementation
- Abandonment of open-source implementations when research funding ended
- No mechanism for learning from deployment (because there is none)
- Aspirational language substituting for demonstrated capability

Boost.Asio exemplifies what GFT calls a live player piloting a functional institution:

- Continuous adaptation to new requirements over twenty years
- Production of derivative works that extend the original vision
- Successful knowledge transfer to subsequent library authors
- A living tradition that survives because practitioners are intrinsically motivated

The choice before WG21 is institutional, not merely technical. Adopting TAPS means betting on a dead player—a specification process that has produced documents but not deployments. Extending Asio means building on a live tradition—two decades of accumulated practice, teaching, and refinement.

History's verdict on this choice is unambiguous. TCP/IP defeated OSI. BSD sockets outlasted every proposed replacement. Proven practice, extended incrementally, consistently outperforms speculative architecture. WG21 should learn from this pattern rather than repeat OSI's mistake with a C++ veneer.

---

## References

1. IETF TAPS Working Group. "Transport Services (taps)." https://datatracker.ietf.org/wg/taps/about/

2. Trammell, B., et al. "An Abstract Application Layer Interface to Transport Services." draft-ietf-taps-interface-26. IETF, 2024.

3. Pauly, T., et al. "Architecture and Requirements for Transport Services." draft-ietf-taps-arch-19. IETF, 2025.

4. Rodgers, T. "A proposed direction for C++ Standard Networking based on IETF TAPS." P3185R0. WG21, 2024.

5. Rodgers, T. and Kühl, D. "Design for C++ networking based on IETF TAPS." P3482R1. WG21, 2025.

6. Kühl, D. "Sender/Receiver Interface For Networking." P2762R0. WG21, 2023.

7. Christensen, A. and Bastien, JF. "Secure Networking in C++." P1861R1. WG21, 2020.

8. Kohlhoff, C. "Boost.Asio." https://www.boost.org/doc/libs/release/doc/html/boost_asio.html

9. NEAT Project. "The EU New, Evolutive API and Transport-Layer Architecture for the Internet." https://www.neat-project.org/

10. APNIC Blog. "Developing a common interface between transport and application layers." January 2021.

11. Apple Developer Documentation. "Network Framework." https://developer.apple.com/documentation/network

12. Fairhurst, G., et al. "Services Provided by IETF Transport Protocols and Congestion Control Mechanisms." RFC 8095. IETF, 2017.

13. Davies, E., ed. "IETF Problem Statement." RFC 3774. IETF, 2004.

14. GeeksforGeeks. "Critique of the OSI Model and Protocols." https://www.geeksforgeeks.org/critique-of-the-osi-model-and-protocols/

15. Graham, R. "Thread on the OSI model is a lie." Errata Security, August 2019.

16. Evans, J. "The OSI model doesn't map well to TCP/IP." https://jvns.ca/blog/2021/05/11/what-s-the-osi-model-/

17. Burja, S. "Great Founder Theory." 2020. https://www.samoburja.com/gft/
