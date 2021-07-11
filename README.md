# Identifying Fraud Rings in bitcoin-otc.com Trust Network - Trying a new approach

## Introduction & Data
Raw data is taken from https://snap.stanford.edu/data/soc-sign-bitcoin-otc.html

This is a trust network of people trading Bitcoin in bitcoin-otc. bitcoin-otc is an over-the-counter
marketplace, i.e. Bitcoin is traded in a p2p fashion. Trust becomes crucial in a place where there is
no one between the buyer and the seller.

## Our Solution (Better than 9 of the 10 well-known algorithms!)*

Basic intuition: Fraud rings consist of fraudster nodes

Approach: Narrow the circle and detect fraud ring members

- Delete low-degree nodes
- Using FxG (Fairness x Goodness) score, get a subgraph of suspected nodes
  - FxG is normally a link predictor with a good accuracy on this data set but we won't use it as a link predictor
- Fraud ring members support each other, so get a subgraph of suspected nodes involved in positive edges
- Detect communities with Louvain Modularity, check if those communities are fraud rings by checking fraudster status of each node
  - Calculate each node's fraudster status using a supervised learning model
    - *This model has 0.89 10-fold CV AUC, outlasting all well-known algorithms except REV2 (See Kumar, 2018)

### Our individual fraud detection approach compared with 10 well-known algorithms:

"On this data set, in terms of 10-fold CV AUC"

- REV2: 0.90
- **Our approach: 0.89**
- FraudEagle: 0.89
- Spamicity: 0.88
- Trustiness: 0.82
- BAD (Bias-and-Deserve): 0.79
- SpamBehavior: 0.77
- ICWSM'13: 0.75
- BIRDNEST: 0.71
- SpEagle: 0.69
- SpEagle+: 0.55


## Key technical decisions
NetworkX and Neo4j will be used in this project instead of {SNAP, iGraph, etc.}
- NetworkX has more network analysis methods than any graph data science library
- Performance issues of NetworkX will be minimal:
    - The data is not high volume (5.8k nodes, 35.6k edges)
    - Neo4j's GDS (Graph Data Science Library) will be used if there's a computationally heavy job
- Neo4j provides a good interface to test your intuition
- Neo4j Bloom is a top notch visualization engine that is very easy to use
- I would use AWS Neptune and their individual fraud detection algorithms if I had enough time to learn them

## How can I reproduce the work?
If you want to fiddle with the data yourself, or if you want to try some operations with different parameters,

- Download Python 3.7, Jupyter Notebooks, and Neo4j 4.1.0
  - For visualization with Neo4j: Use Neo4j Bloom
  - To have more utility with graphs in Neo4j: Install APOC and GDS plugins
- Download the packages in `requirements.txt`
- To load the CSV into Neo4j, use `make_network` function in `sna_bitcoin_otc.utils.network`

## Citations

```text
Kumar, S., Spezzano, F., Subrahmanian, V. S., & Faloutsos, C. (2016). Edge Weight Prediction in Weighted Signed Networks. 2016 IEEE 16th International Conference on Data Mining (ICDM). doi:10.1109/icdm.2016.0033 

Kumar, S., Hooi, B., Makhija, D., Kumar, M., Faloutsos, C., & Subrahmanian, V. S. (2018). REV2. Proceedings of the Eleventh ACM International Conference on Web Search and Data Mining - WSDM ’18. doi:10.1145/3159652.3159729 

Meo, P. D., Musial-Gabrys, K., Rosaci, D., Sarnè, G. M. L., & Aroyo, L. (2017). Using Centrality Measures to Predict Helpfulness-Based Reputation in Trust Networks. ACM Transactions on Internet Technology, 17(1), 1–20. doi:10.1145/2981545 

Thedchanamoorthy, G., Piraveenan, M., Kasthuriratna, D., & Senanayake, U. (2014). Node Assortativity in Complex Networks: An Alternative Approach. Procedia Computer Science, 29, 2449–2461. doi:10.1016/j.procs.2014.05.229 

Hooi, B., Shah, N., Beutel, A., Günnemann, S., Akoglu, L., Kumar, M., … Faloutsos, C. (2016). BIRDNEST: Bayesian Inference for Ratings-Fraud Detection. Proceedings of the 2016 SIAM International Conference on Data Mining. doi:10.1137/1.9781611974348.56
```
