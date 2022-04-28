# Dynamic Flood Risk Model (DFRM)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5506212.svg)](https://doi.org/10.5281/zenodo.5506212)

The global trend of flood damages has been increasing sharply over the past decades due to high population growth and economic activities in floodplain and Bangladesh is experiencing the same.  Though Bangladesh has been able to reduce the loss of life due to floods significantly, but the economic loss and damage have increased manifolds over the decades even at a similar level of hazards. One of the major reasons for this is limited or sometimes no information of flood risk and vulnerability at the community level along with the absence of a timely flood warning system. We present a new tool named “Dynamic Flood Risk Model (DFRM)” for community-level flood warnings which integrates the existing flood prediction (5~10 days) of Flood Forecasting and Warning center (FFWC) of Bangladesh Water Development Board (BWDB) and the results of the 2D hydrodynamic simulation and community-driven flood vulnerability and exposure data. Ultimately, the DFRM model produces a risk-based flood warning which combines the information of flood hazard (flood depth, duration, and velocity) and vulnerability of a system. The tool is developed on a Python platform, where Graphical User Interface (GUI) is designed using the Qt framework. The hazard information is generated through the 2D hydrodynamic simulation of the last three decades flood hydrographs using the Delft3D modelling platform and the vulnerability is estimated from the linear combination of the physical, financial, natural, social, and human capital of the region using secondary and primary data. The model was applied at the village level in two flood-prone districts which were severely flooded by the Brahmaputra-Jamuna, Teesta, and Dharla rivers during the monsoon of 2020. The Synthetic Aperture Radar (SAR) images and local field survey data were used to validate the model-generated hazard and vulnerability information. Comparing of the inundated area from the model and SAR at the union level shows that the accuracy of the model is 91% during the monsoon season. The error margins in pre and post-monsoon seasons are around 5.4% to -9.6%, respectively. The model generated vulnerability was nearly 46% to 50% during the 2020 flood which is also validated by field survey. It is hoped that the successful application of this tool at the community level will enhance the community's resilience and their capability to respond and recover.

## Project Description
**Name :** Developing Institutional Framework for Flood Preparedness Program (FPP)

**Executing agency :** National Resilience Programme (NRP), UNDP

**Funded by :** Ministry of Disaster Management and Relief, Bangladesh

**Research Period :** December 2019 – October 2020

**Research Institutions :** Institute of Water and Flood Management (IWFM), Bangladesh University of Engineering and Technology (BUET)

## Team Member

### Data Analysis, DFRM Design & Development
- [Md. Manjurul Hussain Shourov](https://www.researchgate.net/profile/Md_Manjurul_Shourov)
- [Marin Akter](https://www.researchgate.net/profile/Marin-Akter)

### Delft3d Model Development
- [Md Ashiquir Rahman](https://www.researchgate.net/profile/Md-Ashiqur-Rahman-15)
- [Juwel Islam](https://www.researchgate.net/profile/Juwel-Islam)

### Field Data Collection & Analysis
- [MD Rayhanur Rahman](https://www.researchgate.net/profile/Md-Rahman-228)
- [A K Azad](https://www.researchgate.net/profile/A-Azad-4)
- [Hamima Huma](https://www.researchgate.net/profile/Hamima-Huma)
- Kamrun Nahar
- Sabrina Akther
- Md Shibbir Ahmed

### Supervisor
- [Anisul Haque](https://iwfm.buet.ac.bd/site/faculty/anisul-haque)
- [Md. Munsur Rahman](https://iwfm.buet.ac.bd/site/faculty/md-munsur-rahman)
- [Shampa](https://iwfm.buet.ac.bd/site/faculty/shampa)


<!---
## Citation
You can cite CCM as below :
> Haque, A., Shourov, M.H., Al Azad, A.A., Mita, K.S., Zaman, M.W., Mazhar, S., Ali, M.M., Kabir, R., Ansary, M.A., Ahsan, R. and Rahman, M., (2019) [A Cyclone Classifier Model for Real-time Cyclone Warning in Bangladesh.](http://gadri.net/4gsridrr/4thGlobalSummit_presentations/19gadri4105.pdf) 4th Global Summit of Research Institutes for Disaster Risk Reduction, Kyoto, Japan, March 13-15, 2019

In addition, each release of CCM is achieved on Zenodo with a DOI, that can be found [here](https://zenodo.org/badge/latestdoi/263951347).
-->

## Acknowledgement
This research was a part of a collaborative research project of National Resilience Programme (NRP) between IWFM, BUET and the UNDP funded by Ministry of Disaster Management and Relief, Bangladesh.