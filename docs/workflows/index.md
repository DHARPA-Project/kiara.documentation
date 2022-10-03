# Workflows

This part of the documentation is work in progress, and very bare-bones at the moment.

## Example workflow

*kiara* can render different artefacts from pipeline descriptinos, most notably Jupyter notebooks. This can be done via the command-line:

```
kiara render pipeline logic.xor a=true b=true > xor.ipynb
```

This command looks up the `logic.xor` pipeline operation (you can also specify a pipeline description file -- for example the one created when following [this tutorial](/extending_kiara/pipelines/assemble_pipelines) ), and uses [`Jupyter_notebook.ipynb.j2` from this template folder](https://github.com/DHARPA-Project/kiara/tree/develop/src/kiara/resources/templates/render/pipeline/workflow_tutorial) to render a Jupyter notebook that outlines how to use the *kiara* workflow api via Python. Rendered versions of this example can be found:
- [here](xor)
- or [here]()
