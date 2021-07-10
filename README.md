# Identifying Fraud Rings in bitcoin-otc.com Trust Network

## Introduction & Data
Raw data is taken from https://snap.stanford.edu/data/soc-sign-bitcoin-otc.html

This is a trust network of people trading Bitcoin in bitcoin-otc. bitcoin-otc is an over-the-counter
marketplace, i.e. Bitcoin is traded in a p2p fashion. Trust becomes crucial in a place where there is
no one between the buyer and the seller.

## Problem Definition and Intuition behind the solution

- Edges are directed and signed weighted, an example:
  - A-[:RATED {rating: 3, timestamp: 182346362}]->B

- Individual fraudster nodes receive negative votes (avg. weight of in-degrees are negative)
- Fraud rings tend to vote their "friends" positively but voted negatively by outsiders
- Their centrality would distinguish petty fraudsters from "godfathers"


## Key technical decisions
NetworkX and Neo4j will be used in this project instead of {SNAP, iGraph, etc.}
- NetworkX has more network analysis methods than any graph data science library
- Performance issues of NetworkX will be minimal:
    - The data is not high volume (5.8k nodes, 35.6k edges)
    - Neo4j's GDS (Graph Data Science Library) will be used in computationally heavier jobs whenever possible
- Neo4j Bloom is a top notch visualization engine that is very easy to use

## How can I reproduce the work?
If you want to fiddle with the data yourself, or if you want to try some operations with different parameters,

TBD 

## Citations

```text
Kumar, S., Spezzano, F., Subrahmanian, V. S., & Faloutsos, C. (2016). Edge Weight Prediction in Weighted Signed Networks. 2016 IEEE 16th International Conference on Data Mining (ICDM). doi:10.1109/icdm.2016.0033 

Kumar, S., Hooi, B., Makhija, D., Kumar, M., Faloutsos, C., & Subrahmanian, V. S. (2018). REV2. Proceedings of the Eleventh ACM International Conference on Web Search and Data Mining - WSDM ’18. doi:10.1145/3159652.3159729 

Meo, P. D., Musial-Gabrys, K., Rosaci, D., Sarnè, G. M. L., & Aroyo, L. (2017). Using Centrality Measures to Predict Helpfulness-Based Reputation in Trust Networks. ACM Transactions on Internet Technology, 17(1), 1–20. doi:10.1145/2981545 

Thedchanamoorthy, G., Piraveenan, M., Kasthuriratna, D., & Senanayake, U. (2014). Node Assortativity in Complex Networks: An Alternative Approach. Procedia Computer Science, 29, 2449–2461. doi:10.1016/j.procs.2014.05.229 
```
