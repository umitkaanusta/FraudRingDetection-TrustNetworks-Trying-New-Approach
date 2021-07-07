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
@inproceedings{kumar2016edge,
  title={Edge weight prediction in weighted signed networks},
  author={Kumar, Srijan and Spezzano, Francesca and Subrahmanian, VS and Faloutsos, Christos},
  booktitle={Data Mining (ICDM), 2016 IEEE 16th International Conference on},
  pages={221--230},
  year={2016},
  organization={IEEE}
}

@inproceedings{kumar2018rev2,
  title={Rev2: Fraudulent user prediction in rating platforms},
  author={Kumar, Srijan and Hooi, Bryan and Makhija, Disha and Kumar, Mohit and Faloutsos, Christos and Subrahmanian, VS},
  booktitle={Proceedings of the Eleventh ACM International Conference on Web Search and Data Mining},
  pages={333--341},
  year={2018},
  organization={ACM}
}
```
