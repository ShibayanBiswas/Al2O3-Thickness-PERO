# Reports

This directory contains narrative summaries designed to be copied into a thesis appendix or technical report. The reports emphasize that models are trained on the full dataset by requirement and that all performance values are in sample diagnostics. The writing is intended to connect exported tables and figures to scientific interpretation of thickness response behavior across multiple electrochemical outcomes.

The main artifact is the summary report in Markdown format, which consolidates thickness concentration, correlation diagnostics, model rankings, and per target best model selection. Tables are rendered directly in Markdown so they can be viewed in any editor and committed into report workflows. The report avoids assuming a second feature or a hidden design variable and treats thickness as the only controllable input in the analysis.

When interpreting results, the report highlights the discrete nature of thickness and the heavy concentration at zero thickness. This structure can create apparent step changes that are really group differences rather than smooth continuous trends. The report therefore encourages using grouped summaries, uncertainty bands, and residual structure plots to judge whether observed patterns are robust within thickness levels.

Mathematical notation is expressed using LaTeX style mathtext such as \(R_{\mathrm{ct}}\) and \(Q_{\mathrm{rev}}\) when appropriate, while keeping the prose in consistent Title Case headings. The intention is a PERO style deliverable: polished, export ready, reproducible, and organized so that every plot and table has a clear home and a clear purpose.
