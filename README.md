# SFCL research

Sealed Flow Conditional Liquidity is a proposed research and local-prototype project for Uniswap v4.

## Status
Research specification and analytical checks only. No deployed pool, complete simulation, ZK circuit, production integration or positive LP result is claimed. Funding and timetable are proposed, not awarded.

## Question
Does hiding queued orders before auction bids are fixed improve LP outcomes compared with the same auction and ordering rules with visible orders? The study also tests whether execution-order enforcement, rather than encryption, explains any benefit.

Read PROPOSAL.md for the candidate mechanism, comparisons, proposed milestones and costs.

## Reproduce the analytical check
Run `python3 check_jump_loss.py`. It uses only the Python standard library. The output checks the exact constant-product tangent-benchmark jump loss against its quadratic approximation. It is not a simulation or evidence of SFCL benefit.

## Scope
The proposed work includes model specification, fee-inclusive experiments, a local v4 prototype and a conditional admission-proof study. It does not promise a production launch, a new cryptosystem, perfect flow classification or full LVR recovery.

## Author
Satyawan Singh: https://github.com/ss1738

Public research references are listed in PROPOSAL.md. No private email or prior application response is included in this repository draft. A code licence will be selected before publication.
