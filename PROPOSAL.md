# Sealed Flow Conditional Liquidity

Research and prototype proposal

Satyawan Singh | 14 November 2026 | Proposed request USD 90,000

Repository: https://github.com/ss1738/sfcl-research (MIT licence)

Proposed delivery period: 26 weeks. Cost estimate: 900 hours at $100 per hour. GUESS: Hours and rate are proposed estimates, not measured implementation costs. I will allocate approximately 35 hours per week over the proposed delivery period.

## What I propose

I propose to study and prototype Sealed Flow Conditional Liquidity (SFCL), a Uniswap v4 execution mechanism that combines encrypted order submission with auctioned rebalancing rights. I will test whether the combination improves liquidity provider (LP) outcomes after accounting for execution costs, informed orders, weak auction competition and delayed settlement.

I will carry out the work myself. The funded outputs will be a mechanism specification, economic model, reproducible experiments and a local v4 prototype. Zero-knowledge (ZK) admission will have a separate decision gate: I will implement a bounded proof prototype only if checking the policy before decryption serves a demonstrated purpose.

## The question to answer

Does keeping queued orders confidential until bids and execution order are fixed improve LP outcomes compared with the same auction and execution rules with visible orders? A second question is whether enforcing the execution order accounts for any benefit attributed to encryption.

INFERRED: Encryption can hide information about queued orders, but it does not hide external market prices from searchers. It may reduce information-based extraction, reduce what bidders are willing to pay, or have no net benefit. The experiments will distinguish these outcomes.

## Who benefits

The work is intended for v4 researchers, hook developers and liquidity managers assessing execution mechanisms. I will publish the model, source code, experiment settings and findings, including failures. The benefit to the Uniswap ecosystem is a published, rerunnable answer to whether this mechanism class is worth building on v4, measured by net LP outcomes against a defined rebalancing benchmark. Original code will be released under the MIT licence. This phase does not include a production launch, liquidity subsidy, new token or finalised standard.

## Existing work

MEASURED: v4 provides hooks and custom accounting [1]. Several designs already address LP loss or user-level extraction. I do not claim any of them as new, and for [2], [8], [9] and [10] I read the abstracts and the sections cited here, not the full papers.

MEASURED: am-AMM auctions the right to manage a pool through an onchain auction. Its authors note it may protect less against sandwich attacks than a fixed-fee pool, because the manager can push publicly visible transactions to their limit price [2]. FM-AMM batches trades and reports that competition between arbitrageurs removes arbitrage profit and sandwich attacks, under the assumption that trades are batched [8]. V0LVER combines an encrypted mempool with an AMM in which orders are decrypted after being allocated liquidity, and notes that naive batching still lets a block producer extract loss-versus-rebalancing (LVR) by censoring orders [9]. Shutter documents threshold release conditions [3].

MEASURED: A 2026 survey of encrypted mempools concludes that blind ordering with all-or-nothing decryption suppresses the same-block auctions that return value to users, and that an auction run after decryption comes too late [10]. SFCL is a candidate answer to that limitation, not a refutation of it: searchers bid before the batch is revealed, and the batch order is committed first.

Reviewed from public descriptions only, with full review left to M1: Angstrom is a v4 hook in which an off-chain sequencer network runs auctions on aggregated order flow and settles at a uniform clearing price [11]. Arrakis published a v4 hook proof of concept in which the block builder commits a price and the tokens removed from the pool are re-added gradually over later blocks [12]. Unichain builds blocks in a trusted execution environment (TEE) with priority-fee ordering. Its announcement describes a private encrypted mempool and also lists encrypted mempools as a future upgrade, so the current status needs confirming [13].

INFERRED: The open question is narrow. It is whether an auction over hidden, order-committed flow adds net LP benefit beyond the same rules with visible orders (B), and beyond simpler defences such as batching, am-AMM style rights or TEE ordering. Bidders who cannot see the batch may bid low, and a TEE-based approach may dominate. Either result is acceptable. M1 will compare the proposed rights and timing with each source above and will stop or narrow the work if the candidate is duplicative.

## Candidate mechanism and comparisons

## One execution cycle

The initial model uses fixed-duration epochs. Before the bid deadline, users submit signed swap intents with an amount limit, expiry, recipient and nonce. A batch commitment fixes the admitted ciphertexts and their execution order. The commitment is part of the modelled protocol, not an assumed production sequencer feature.

Searchers bid for one exclusive rebalancing opportunity after the committed user batch. They bid before the encrypted batch is revealed. The auction is sealed-bid and first-price, with a stated reserve and payment escrow. The winner must fund the payment before obtaining the right. Payment is allocated to LP capital exposed during that epoch.

After release, the batch executes in the committed order with each intent’s stated limits. The winner can then execute one permitted rebalancing transaction. The initial model gives the winner no right to insert trades inside the batch. A bounded execution window, collateral, default penalties and fallback behaviour will be specified in the first milestone and varied in experiments.

The local prototype will restrict the modelled pool entry points. Experiments will separately introduce policy-compliant informed orders, order splitting and unauctioned access. Isolation in a simulator will not be presented as proof that arbitrage can be excluded in production.

## Controlled comparisons

| Case | Rules | Information |

| --- | --- | --- |

| A | Ordinary pool with explicitly stated fees | Visible orders |

| B | Committed batch plus rebalancing auction | Orders visible before bids |

| C | Same timing and execution rules as B | Orders hidden until bids and ordering are fixed |

| D | Variant of C with permitted post-reveal insertion | Tests dependence on execution enforcement |

B versus C isolates pre-bid confidentiality. C versus D tests ordering protection. A versus B tests the auction and batching changes together. Offered flow, price paths, initial capital, fees and costs will be matched where the mechanism permits; different fills will be reported rather than hidden.

## When the model fails

Release failure, winner default, user expiry, rejected intents and batch abandonment will have separate outcomes. The model will report locked capital, refunds, execution losses and penalties. No silent fallback from exposed orders to an unprotected public queue is assumed.

## Research method and technical limits

## Economic evaluation

Use a full-range constant-product pool first, with an exact fee-free analytical check and an explicitly fee-inclusive execution model. Concentrated liquidity will be a separately identified extension. Evaluate diffusion, finite-activity jumps and stress jumps; vary external-price information, trader demand, bidder count, costs, bid suppression and settlement delay.

Measure LP wealth relative to a defined rebalancing benchmark, auction payments, residual adverse selection, fees, execution costs, capital use, user execution quality and unfilled volume. Decompose transfers between participants so higher auction receipts are not confused with improved total execution.

Publish configurations, source revisions and paired random seeds. Report uncertainty and parameter sensitivity. Synthetic order-flow results will be identified as synthetic; they will not establish adoption or production returns.

## Cryptographic boundary

INFERRED: A size proof establishes a policy predicate, not that a trader lacks information. Historical correlation will not be an admission input without an authenticated definition and a completeness assumption. Public checks after decryption, deposits and rate limits are mandatory comparisons before choosing ZK.

For a proof prototype, bind the admitted intent to the ciphertext and executed parameters, with replay protection and chain, pool, policy and epoch separation. Specify integer bounds, encodings, commitment randomness and setup assumptions. Measure the complete witness/proving path and integrated verification cost rather than extrapolate from a range-check circuit.

Threshold confidentiality assumes fewer than the required number of members collude early. Availability separately requires enough valid shares by the deadline. The local harness will inject early release and withholding. A new threshold cryptosystem is outside scope; any library integration will name its version and assumptions.

## Mathematical benchmark

INFERRED: For fee-free full-range value V(p)=K sqrt(p), a relative jump z greater than -1 gives tangent-benchmark loss V(p)[1+z/2-sqrt(1+z)]. Its quadratic small-jump approximation is V(p)z²/8. I will use the exact expression to check the simulator and report approximation error. It is not a general formula for delayed or concentrated-liquidity execution [4].

## Continuation criteria

Before the main runs, publish representative scenarios, stress cases and numerical decision thresholds. Continue toward integration only if confidentiality adds positive net LP benefit over B in the agreed cases, with trader trade-offs disclosed. If not, publish the negative result and recommend the simpler mechanism. A code prototype is not evidence of economic benefit.

## Milestones and budget

All work is allocated to Satyawan Singh. No hired engineer, paid external reviewer or third-party endorsement is promised. GUESS: The effort estimates below total 900 hours at a proposed $100 per hour. No separate infrastructure or audit allowance is requested.

| Milestone | Period | Hours | USD |

| --- | --- | --- | --- |

| M1 Specification and prior art | Weeks 1 to 4 | 120 | 12,000 |

| M2 Economic model and baseline harness | Weeks 5 to 10 | 220 | 22,000 |

| M3 v4 local prototype and failure tests | Weeks 11 to 18 | 280 | 28,000 |

| M4 Conditional proof study and final report | Weeks 19 to 26 | 280 | 28,000 |

| Total | 26 weeks | 900 | 90,000 |

## M1 acceptance

Publish the prior-art comparison, auction entitlement, bid and release timing, settlement/default state machine, LP premium allocation, threat model and experiment protocol. Identify production capabilities that remain unavailable or unverified. If the candidate is duplicative or cannot support a meaningful comparison, publish that finding and propose a scope change before further work.

## M2 acceptance

Publish runnable A to D comparisons, analytical validation cases, explicit fees and costs, adversarial agents, parameter files and initial results. Independent reruns must be possible using documented commands. Acceptance does not depend on showing a positive result.

## M3 acceptance

Publish a local v4 prototype and tests for authorisation, replay, escrow, premium attribution, entry/exit timing, timeouts and recovery. Report which execution guarantees are enforced locally and which require external support. This is an experimental prototype, not an audited production deployment.

## M4 acceptance

Publish the admission-proof decision and evidence. If justified, implement and benchmark a bounded proof relation; otherwise publish the simpler-defence comparison. Deliver the final findings, limitations, reproduction instructions and recommendation. Invite technical feedback and record responses without promising third-party review or endorsement.

Milestone payments are proposed allocations tied to these outputs, subject to the grant agreement. A negative research result can satisfy a milestone if the specified experiments and evidence are delivered. Any major scope change will be agreed before the affected work proceeds.

## Experience and references

## Relevant experience

I am Satyawan Singh. I will own the specification, model, prototype, experiments and report.

MEASURED: My Sui PR 28208 is marked merged and concerns Byzantine equivocation testing in the randomized consensus DAG harness [5]. My GitHub profile is https://github.com/ss1738 .

MEASURED: My earlier HookSwap application described Solidity fork testing, event/receipt analysis and Python data processing. Its public project link is https://github.com/ss1738/hookswap-kit . The submitted metrics are not reused as SFCL results.

## Funding and current status

MEASURED: CoW approved a separate $2,000 DAI signed-order conformance grant on 8 October 2026 [6]. M1 is tracked in PR 63 [7]. Approval is not presented as completed delivery or payment. No CoW deliverable or completed HookSwap work is charged to this request.

SFCL is pre-launch research. No SFCL deployment, independent use, positive LP result or measured proving performance is claimed. This request funds the research and local prototype described here. Publication does not imply a production security guarantee. The mechanism uses temporary confidentiality of submitted intents, which I disclose for any privacy-related review. No shielded balances or token issuance are proposed.

## References

[1] Uniswap v4 architecture. https://developers.uniswap.org/docs/protocols/v4/concepts/architecture

[2] Adams et al. am-AMM. https://arxiv.org/abs/2403.03367

[3] Shutter threshold release. https://docs.shutter.network/docs/protocol/api/how_it_works

[4] Milionis et al. Automated Market Making and Loss-Versus-Rebalancing. https://arxiv.org/abs/2208.06046

[5] Sui contribution. https://github.com/MystenLabs/sui/pull/28208

[6] CoW approval. https://forum.cow.fi/t/3569/15

[7] CoW M1 PR. https://github.com/cowdao-grants/cow-rs/pull/63

[8] Canidio and Fritsch. Arbitrageurs' profits, LVR, and sandwich attacks: batch trading as an AMM design response. https://arxiv.org/abs/2307.02074

[9] McMenamin and Daza. An AMM minimizing user-level extractable value and loss-versus-rebalancing (V0LVER). https://arxiv.org/abs/2301.13599

[10] Passerat-Palmbach. SoK: Encrypted Mempools Through the MEV Lens. https://eprint.iacr.org/2026/1643

[11] Uniswap Foundation. Builder stories: Yuki Yuminaga on ASS and Angstrom, 21 January 2025. https://uniswapfoundation.org/blog/builder-stories-yuki-yuminaga-on-ass-and-angstrom

[12] Arrakis Finance. Diamond hook proof of concept, code walkthrough. https://github.com/ArrakisFinance/minimize-lvr-hook-poc

[13] Uniswap Labs. Rollup-Boost is live on Unichain. https://blog.uniswap.org/rollup-boost-is-live-on-unichain
