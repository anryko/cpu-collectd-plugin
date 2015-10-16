# cpu-collectd-plugin

Collectd linux CPU states tracking plugin.

#### Motivation
Default CollectD CPU plugin graphing is complicated. Plugin stores information per thread which is not relevant to my use case and in case when I have 32 threads on the machine it takes quite a while to query 8x32 metrics. I want to have aggregated metrics in 'percent' ready to graph.

#### Metrics
```
user
nice
system
idle
wait
interrupt
softirq
steal
guest
guestn
```
