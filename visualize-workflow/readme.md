Visualize Workflows
===================

This is a simple tool for visualizing workflow operation processing times. It
helps you identify bottlenecks in your workflow by putting the processing time
of single operations into a visual context.

Usage
-----

First, set your system's location and digest login credentials in
`./get-workflow.sh`.

Then, get the identifier for the workflow you want to visualize from the event
details of Opencast's admin interface.

Finally, Run the tool-chain (this example uses the workflow identifier 1666):

```bash
./get-workflow.sh 1666
./prep-workflow.py
gnuplot plot-workflow.gnuplot
```

This will produce a `workflow.svg`.
