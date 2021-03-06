#%%
import markdown
from IPython.core.display import display, HTML
def md(str):
    display(HTML(markdown.markdown(str + "<br />")))

#%%
md("""
# 6 Multi-order Representation Learning

**Ingo Scholtes**  
Data Analytics Group  
Department of Informatics (IfI)  
University of Zurich  


**September 5 2018**

So far, we studied higher-order network models for path data with a fixed, given order $k$. We have seen that such higher-order models can yield better predictions compared to standard network models. But we also came across new questions: For the US Flight data, we could improve the prediction performance by moving from a first- to a second-order model. However, we did not see a further improvement for the third-order model. So in practice, how can we decide **at which order we should model a given system**? This points to a more general question as we can also imagine systems for which path statistics do not deviate significantly from the transitive, Markovian assumption made by a first-order model. So we **need methods to decide when higher-order models are actually needed**.

Moreover, a higher-order model with order $k$ can only capture higher-order dependencies at a single fixed correlation length $k$. But we may encounter data that exhibit multiple correlation lengths at once. How can we **combine models with multiple higher orders into a multi-order model**?

In this unit, we take a statistical inference and machine learning perspective to answer these questions. To show how the method works, we again start with a maximally simple toy example:

<span style="color:red">**TODO:** Import the package `pathpy` and rename it to `pp`. Create a new instance `p` of class `Paths` and add two paths $a \rightarrow c \rightarrow d$ and $b \rightarrow c \rightarrow e$, each occurring twice.</span>
""")

#%% In [1]
import pathpy as pp

toy_paths = pp.Paths()
toy_paths.add_path('a,c,d', 2)
toy_paths.add_path('b,c,e', 2)
print(toy_paths)

#%%
md("""
As mentioned before, in this example we only observe two of the four paths of length two that would be possible in the null model. Hence, this is an example for path statistics that exhibit correlations that warrant a second-order model. 

But how can we decide this in a statistically sound way? We can take a statistical inference perspective on the problem. More specifically, we will consider our higher-order networks as probabilistic generative models for paths in a given network topology. For this, let us use the weighted first-order network model to construct a transition matrix of a Markov chain model for paths in a network. We simply use the relative frequencies of edges to proportionally scale the probabilities of edge transitions in the model.

<span style="color:red">**TODO:** Generate a first-order model of `toy_paths`. Plot the model and print the transition matrix generated by the method `HigherOrderNetwork.transition_matrix`.</span>
""")

#%% In [2]
hon_1 = pp.HigherOrderNetwork(toy_paths)
pp.visualisation.plot(hon_1)
print(hon_1.transition_matrix())

#%%
md("""
This transition matrix can be viewed as a first-order Markov chain model for paths in the underlying network topology. This probabilistic view allows us to calculate a likelihood of the first-order model, given the paths that we have observed. With `pathpy`, we can directly calculate the likelihood of a higher-order model, given a `Paths` instance.

<span style="color:red">**TODO:** Use the `HigherOrderNetwork.likelihood` method to calculate the likelihood of the first-order model given `toy_paths`. Set the parameter `log` to False.</span>
""")

#%% In [3]
print(hon_1.likelihood(toy_paths, log=False))

#%%
md("""
This result is particularly easy to understand for our toy example. Each path of length two corresponds to two transitions in the transition matrix of our Markov chain model. For each of the four paths of length two in `toy_paths`, the first transition is deterministic because nodes $a$ and $b$ only point to node $c$. However, based on the network topology, for the second step we have a choice between nodes $d$ and $e$. Considering that we see as many transitions through edge $(c,d)$ as we see through edge $(c,e)$, in a first-order model we have no reason to prefer one over the other, so each is assigned probability $0.5$.

Hence, for each of the four observed paths we obtain a likelihood of $1 \cdot 0.5 = 0.5$, which yields a total likelihood for four (independent) observations of $0.5^{4} = 0.0625$.
""")

#%%
md("""
Let us compare this to the likelihood of a second-order model for our paths.

<span style="color:red">**TODO:** Generate a second-order model for `toy_paths` and print the transition matrix. Use the `HigherOrderNetwork.likelihood` method to calculate the likelihood of a second-order model, given `toy_paths`.</span>
""")

#%% In [4]
hon_2 = pp.HigherOrderNetwork(toy_paths, k=2)
print(hon_2.transition_matrix())
hon_2.likelihood(toy_paths, log=False)

#%%
md("""
Here, the likelihood assumes its maximal value of $1.0$, simply because all transitions in the second-order model are deterministic, i.e. we simply multiply $1 \cdot 1$ four times. 

Let us now have a look at the *second-order null model*, which is actually a first-order model represented in the second-order space. So we should expect the same likelihood as the first-order model.

<span style="color:red">**TODO:** Generate a second-order null model for `toy_paths` and print the transition matrix. Use the `HigherOrderNetwork.likelihood` method to calculate the likelihood of this model, given `toy_paths`.</span>
""")

#%% In [5]
hon_2_null = pp.HigherOrderNetwork(toy_paths, k=2, null_model=True)
pp.visualisation.plot(hon_2_null)
print(hon_2.transition_matrix())
hon_2_null.likelihood(toy_paths, log=False)

#%%
md("""
### Model selection for higher-order network models

Clearly, the second-order null should have the same likelihood as the first-order model. This also shows a way to test hypotheses about the presence of higher-order correlations in paths. We can use a likelihood ratio test to compare the likelihood of the null hypothesis (i.e. a second-order representation of the first-order model) with the likelihood of an alternative hypothesis (the *fitted* second-order model).

But what do we learn from the fact that the likelihood of a model increases as we increase the order of the model. By itself, not much. Higher-order models are more complex than first-order models, i.e. while fitting their transition matrix we actually fit more parameters to the data. We can thus expect that such a more complex model better explains our (path) data. 

We should remind ourselves about Occam's razor, which states that we should favor models that make fewer assumptions. That is, in the comparison of the model likelihoods we should account for the additional complexity (or degrees of freedom) of a higher-order model over the null hypothesis.

A nice feature of our framework is that the null model and the alternative model are actually **nested**, i.e. the null model is one particular point in the parameter space of the (more general) higher-order model. Thanks to this property, we can apply [Wilk's theorem](https://en.wikipedia.org/wiki/Likelihood-ratio_test#Distribution:_Wilks’_theorem) to derive an analytical expression for the $p$-value of the null hypothesis that second-order correlations are absent (i.e. that a first-order model is sufficient to explain the observed paths), compared to the alternative hypothesis that a second-order model is needed. You can find the full mathematical details of this hypothesis testing approach in the following KDD'17 paper:

I Scholtes: [When is a Network a Network? Multi-Order Graphical Model Selection in Pathways and Temporal Networks](http://dl.acm.org/citation.cfm?id=3098145), In KDD'17 - Proceedings of the 23rd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, Halifax, Nova Scotia, Canada, August 13-17, 2017

Let us apply this to test the hypothesis that there are **significant** second-order dependencies in our toy example. This test consists of three basic steps: 

1. We calculate the difference $d$ between the parameters (or degrees of freedom) of a second- and a first-order model.
2. We calculate the test statistic $x = -2 \cdot(\log(\text{hon_1.likelihood}) - \log(\text{hon_2.likelihood}))$ for the likelihood ratio test.
3. We calculate a p-value as $1-cdf(x, d)$, where $cdf$ is the cumulative distribution function of a chi-square distribution.

<span style="color:red">**TODO:** Perform the likelihood ratio test for the null hypothesis that the observed paths can be explained by a first-order model. Use the function `HigherOrderNetwork.degrees_of_freedom` to calculate the degrees of freedom of a k-th order model. Use `chi2.cdf` from `scipy.stats` to calculate the p-value.</span>
""")

#%% In [6]
from scipy.stats import chi2

d = hon_2.degrees_of_freedom() - hon_1.degrees_of_freedom()
x = - 2 * (hon_1.likelihood(toy_paths, log=True) - hon_2.likelihood(toy_paths, log=True))
p = 1 - chi2.cdf(x, d)

print('The p-value of the null hypothesis (first-order model) is {0}'.format(p))

#%%
md("""
The $p$-value of the null hypothesis that we can explain the four observed paths based on the weighted network topology alone is (borderline) 0.019. This is intuitive, as we have only observed four paths, which is hardly enough to robustly reject a first-order network model. Let us see what happens if we observe those same paths more often.

<span style="color:red">**TODO:** Use the arithmetic operators defined on `Paths` to multiply all observation counts with ten. Repeat the likelihood ratio test and output the p-value.</span>
""")

#%% In [7]
toy_paths *= 10

x = - 2 * (hon_1.likelihood(toy_paths, log=True) - hon_2.likelihood(toy_paths, log=True))
p = 1 - chi2.cdf(x, d)

print('The p-value of the null hypothesis (first-order model) is {0}'.format(p))

#%%
md("""
So, if we were to observe each of the two paths four time, we would reject the null hypothesis because it is very unlikely to not observe two of the four possible paths a single time in eight observations. If we were to further increase the number of observations of the two paths the p-value decreases.

Unofortunately, the toy example above is too simple in multiple ways: First, it only contains paths of exactly length two, thus justifying a second-order model. But real data are more complex, as we have observations of paths at multiple lengths simultaneously. Such data are likely to exhibit multiple correlation lengths at the same time.

Even more importantly, in real data the model selection will unfortunately not work as described above. In fact, I have cheated because we cannot - in general - directly compare likelihoods of models with different order. The following example highlights this problem:

<span style="color:red">**TODO:** Create an empty `Paths` instance and add the following path:</span>

`('a','b','c','d','e','c','b','a','c','d','e','c','e','d','c','a')`

<span style="color:red">Generate a first-order model, as well as a second- and fifth-order **null** model for the data. Compare the likelihoods between the three models.</span>
""")

#%% In [8]
path = ('a','b','c','d','e','c','b','a','c','d','e','c','e','d','c','a')

p = pp.Paths()
p.add_path(path)
pp.visualisation.plot(pp.Network.from_paths(p))

hon_1 = pp.HigherOrderNetwork(p, k=1)
hon_2 = pp.HigherOrderNetwork(p, k=2, null_model=True)
hon_5 = pp.HigherOrderNetwork(p, k=5, null_model=True)

print(hon_1.likelihood(p, log=False))
print(hon_2.likelihood(p, log=False))
print(hon_5.likelihood(p, log=False))

#%%
md("""
This is strange! Shouldn't the likelihoods of these three models be identical? They are not, and this is a major issue when we have data that consists of large numbers of short paths: in terms of the number of transitions that enter the likelihood calculation, a model of order $k$ discards the first $k$ nodes on each path. That is, a second-order model can only account for all but the first edge traversals on the path. This means that - in the general case - we actually compare likelihoods computed for different sample spaces, which is not valid.

<span style="color:red">**TODO:** Calculate the number of transitions involved in the likelihood calculation of each model.</span>
""")

#%% In [9]
print('Path consists of {0} nodes'.format(len(path)))
print('Number of transitions in  first-order model = ', str(len(hon_1.path_to_higher_order_nodes(path)[1:])))
print('Number of transitions in second-order model = ', str(len(hon_2.path_to_higher_order_nodes(path)[1:])))
print('Number of transitions in  fifth-order model = ', str(len(hon_5.path_to_higher_order_nodes(path)[1:])))

#%%
md("""
### Multi-order representation learning

To fix the issues above, we need a probabilistic generative model that can deal with large collections of (short) paths in a network. The key idea is to combine multiple higher-order network models into a single multi-layered, multi-order model. To calculate the likelihood of such a model we can use all layers, thus avoiding the problem that we discard prefixes of paths. For each path, we start the calculation at a layer of order zero, which considers the relative probabilities of nodes. We then use this model layer to calculate the probability to observe the first node on a path. For the next transition to step two, we then use a first-order model. The next transition is calculated in the second-order model and so on, until we have reached the maximum order of our multi-order model. At this point, we can transitively calculate the likelihood based on the remaining transitions of the path.

The method is described in all details in the following paper:

I Scholtes: [When is a Network a Network? Multi-Order Graphical Model Selection in Pathways and Temporal Networks](http://dl.acm.org/citation.cfm?id=3098145), In KDD'17 - Proceedings of the 23rd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, Halifax, Nova Scotia, Canada, August 13-17, 2017

But let us go to practice. `pathpy` can directly generate, visualise, and analyse multi-order network models. Let us try this in our example.

<span style="color:red">**TODO:** Create an instance of class `MultiOrderModel` and fit it to the `toy_paths` example from above. Use the method `pp.visualisation.plot` to visualise the entries of `MultiOrderModel.layers` for the the resulting instance.</span>
""")

#%% In [10]
mog = pp.MultiOrderModel(toy_paths, max_order=2)
print(mog)

pp.visualisation.plot(mog.layers[0])
pp.visualisation.plot(mog.layers[1])
pp.visualisation.plot(mog.layers[2])

#%%
md("""
We can now use the `likelihood` function of the class `MultiOrderModel` to repeat our likelihood ratio test. Rather than generating multiple `MultiOrderModel` instances for different hypotheses, we can directly calculate likelihoods based on different model layers within the same `MultiOrderModel` instance.

<span style="color:red">**TODO:** Repeat the likelihood ratio test from above, comparing the likelihoods of a multi-order model. Utilise the fact that you can pass a parameter `max_order` to the `MultiOrderModel.likelihood` method, which specifies the maximum order to use in the likelihood calculation.</span>
""")

#%% In [11]
mog = pp.MultiOrderModel(toy_paths, max_order=2)

d = mog.degrees_of_freedom(max_order=2) - mog.degrees_of_freedom(max_order=1)
x = - 2 * (mog.likelihood(toy_paths, log=True, max_order=1) - mog.likelihood(toy_paths, log=True, max_order=2))
p = 1 - chi2.cdf(x, d)

print('p value of null hypothesis that data has maximum order 1 = {0}'.format(p))

#%%
md("""
Based on this p-value, we would again reject the null hypothesis that the paths can be explained by a first-order network model. We now actually get a different p-value, as we also account for a zero-order model, i.e. we account for the relative frequencies at which nodes occur at the start of a path.

Rather than performing the likelihood test ourselves, we can actually simply call the method `MultiOrderModel.estimate_order`. it will return the maximum order among all of its layers for which the likelihood ratio test rejects the null hypothesis.

<span style="color:red">**TODO:** Use the `MultiOrderModel.estimate_order` method to learn the optimal order in the `MultiOrderModel` from above.</span>
""")

#%% In [12]
mog.estimate_order()

#%%
md("""
We now test whether this approach to **learn the optimal representation of path data** actually works. For this, let us generate path statistics that are in line with what we expect based on a first-order network model, and check whether the order estimation gives the right result.

<span style="color:red">**TODO:** Create a `Paths` instance with path statistics that conform to a first-order model, for a `MultiOrderModel` and return the optimal maximum order of the model.</span>
""")

#%% In [13]
random_paths = pp.Paths()
random_paths.add_path('a,c,d', 5)
random_paths.add_path('a,c,e', 5)
random_paths.add_path('b,c,e', 5)
random_paths.add_path('b,c,d', 5)

mog = pp.MultiOrderModel(random_paths, max_order=2)
print('Optimal order = ', mog.estimate_order(random_paths))

#%%
md("""
### Multi-order network visualisation

Conveniently, the `MultiOrderModel.layers` dictionary contains `HigherOrderModel` instances, that we can use to analyse data at a given order $k$. Moreover, we can use the higher-order network layout algorithm introduced in the previous unit to visualise the causal topology of a system. 

However, in the previous example we have seen that such visualisations only consider the causal topology at a single correlation length $k$. For real data, we rather want a visualisation that merges information from multiple correlation lengths. We can actually use the `MultiOrderModel` to address this issue. For this, we can simply plot a `MultiOrderModel` instance. Let us demonstrate this in a toy example where we have multiple correlation lengths at the same time.

<span style="color:red">**TODO:** Generate a multi-order model with maximum order three for a toy example with two paths $a \rightarrow c \rightarrow d \rightarrow f$ and $b \rightarrow c \rightarrow d \rightarrow g$, each appearing five times. Estimate the optimal maximum order of the multi-order model.</span>
""")

#%% In [14]
p = pp.Paths()
p.add_path('a,c,d,f', 5)
p.add_path('b,c,d,g', 5)

m = pp.MultiOrderModel(p, max_order=3)
print('Optimal maximum order is {0}'.format(m.estimate_order()))

#%%
md("""
It is easy to see that this is correct. Due to the chain of two nodes $c$ and $d$ on the paths, a second-order model has no chance to detect the dependency between the origin and the destination of the paths. We need a third-order model to see that the path statistics deviates from a network model. 

We can now generate a higher-order visualisation of the three model layers as shown in the previous unit.

<span style="color:red">**TODO:** Apply the `pp.visualisation.plot` method on the layers of the multi-order model to generate a higher-order network visualisation. Make sure to set the `plot_higher_order_nodes` parameter to `False`.</span>
""")

#%% In [18]
pp.visualisation.plot(m.layers[1], plot_higher_order_nodes=False)
pp.visualisation.plot(m.layers[2], plot_higher_order_nodes=False)
pp.visualisation.plot(m.layers[3], plot_higher_order_nodes=False)

#%%
md("""
Considering the paths from which the higher-order models where created, it is easy to understand these higher-order visualisations. In the first-order model, we only consider the topology of links to calculate the force-directed layout. In the second-order model, we account for the fact that we observe (sub-)paths of length two between nodes $a, d$ and $b,d$, as well as between $c,f$ and $c,g$. This structure of the paths leads to the *clustered* layout above, because the second-order layout does not account for the first-order topology. Similarly, the third-order layout places nodes $a$ and $f$ as well as $b$ and $g$ close to each other, since paths of length three connect those pairs of nodes. 

But neither of these layouts is ideal, if we want to understand the relevant structures in the causal topology of the graph. We rather want to combine the layout information of the different orders. `pathpy` can do that for you. We only need to pass a `MultiOrderModel` instance instead of a a `HigherOrderNetwork` instance to the `plot` function. This will lead to a layout in which forces are calculated using all layers of the `MultiOrderModel`.

<span style="color:red">**TODO:** Apply the `pp.visualisation.plot` method on the multi-order model. Make sure to set the `plot_higher_order_nodes` parameter to `False`.</span>
""")

#%% In [16]
pp.visualisation.plot(m, plot_higher_order_nodes=False)

#%%
md("""
The resulting network layout is more meaningful than any of the layouts above. If you drag the nodes, you will see that there is an attractive force between nodes $a$ and $f$ and $b$ and $g$, while the pairs across repel each other. Compared to the first-order layout above, this visualised the causal structures in the paths, while avoiding the problems of the higher-order layouts.
""")

