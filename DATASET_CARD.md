---
language:
- en
license: mit
task_categories:
- tabular-classification
tags:
- economics
- frictionshift
- computational-economics
- platform-economics-digital-markets
- emerging-terminology
pretty_name: Frictionshift Economics Dataset
size_categories:
- n<1K
---

# Frictionshift Economics Dataset

## Dataset Description
### Summary
Synthetic 200-row dataset for `Frictionshift` measurement and computational experiments.

### Supported Tasks
- Economic analysis
- Platform Economics / Digital Markets research
- Computational economics

### Languages
- English (metadata and documentation)
- Python (code examples)

## Dataset Structure
### Data Fields
- `id`: Unique observation id
- `journey`: Synthetic customer journey cohort
- `entry_friction_relief`: Reduction in onboarding friction at entry stage
- `mid_journey_friction`: Friction introduced during service usage steps
- `exit_friction`: Friction imposed at cancellation or switching stage
- `hidden_fee_intensity`: Intensity of non-salient deferred fees
- `switching_penalty`: Penalty magnitude for platform exit/switch
- `cancellation_cost`: Economic and time cost of cancellation process
- `transparency_level`: Transparency of full lifecycle costs
- `frictionshift_index`: Composite term index

### Data Splits
- Full dataset: 200 examples

## Dataset Creation
### Source Data
Synthetic data generated for demonstrating Frictionshift applications.

### Data Generation
Channels are sampled from controlled distributions with correlated structure. The term index is computed from normalized channels and directional weights.

## Considerations
### Social Impact
Research-only synthetic data for method development and reproducibility testing.

## Additional Information
### Licensing
MIT License - free for academic and commercial use.

### Citation
@dataset{frictionshift2026,
title={{Frictionshift Economics Dataset}},
author={{Economic Research Collective}},
year={{2026}}
}
