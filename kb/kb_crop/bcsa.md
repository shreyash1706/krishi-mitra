# Development and Evaluation of Nutrient Expert® Decision Support Tool for Cereal Crops

By Mirasol F. Pampolino, Christian Witt, Julie Mae Pasuquin, Adrian M. Johnston, and Myles J. Fisher

**Nutrient Expert® (NE) is a computer-based decision support tool that uses the principles of site-specific nutrient management for developing fertiliser recommendations tailored to a specific field or growing environment. Results of field evaluation have shown that NE is effective in providing recommendations that can increase yields and profits compared with farmers’ current practices. NE accounts for the important factors affecting site-specific recommendations, which makes it an excellent tool for providing tactical information to crop advisors and farmers as well as strategic information to high-level decision makers. NE is also a suitable starting point for developing nutrient management tools to reach more users.**

The demand for increased cereal production to feed an increasing world population will not be met just by the expansion in cultivated area, but more by intensifying production of wheat, rice and maize. Currently, cereal yields are only 40 to 65% of their potential, mostly because nutrient management does not consider crop’s dynamic response to the environment. Intensification will therefore need nutrient management that produces high yields, while preserving soil quality and protecting the environment.

Site-specific nutrient management (SSNM) is a set of nutrient management principles, which aims to supply a crop’s nutrient requirements tailored to a specific field or growing environment. Although SSNM has been proven to increase yields and productivity in on-farm trials, there has been little acceptance. The reason being many extension agents still perceive SSNM as complex, requiring an understanding of concepts and methods outside their experience. A simple nutrient decision support tool based on the principles and guidelines of SSNM, such as Nutrient Expert® (NE), will help crop advisors develop strategies to manage fertiliser N, P and K tailored to a farmer’s field or growing environment. As a computer-based decision support tool, NE combines all the steps and guidelines in SSNM into a simple software tool tailored for crop advisors, especially the not-so-technical users such as the extension agents in developing countries.

The conceptual framework used in the development of NE is applicable to any cereal crop and geographic location. The algorithm for calculating fertiliser requirements in NE is determined from a set of on-farm trial data using SSNM guidelines. In SSNM, the N, P and K requirements are based on the relationships between balanced uptake of nutrients at harvest and grain yield (Buresh et al., 2010; Setiyono et al., 2010). This

> **Abbreviations and notes: N = nitrogen; P = phosphorus; K = potassium.**

The image shows a group of four people standing in a field in front of a large informational signboard. The signboard displays logos for CSISA, CIMMYT, IPNI, the Bill & Melinda Gates Foundation, and USAID. It also contains details about a research trial:

**CEREAL SYSTEMS INITIATIVE FOR SOUTH ASIA**

<table>
  <tbody>
    <tr>
        <td>Title of the experiment: Nutrient management in maize raised under different tillage practices</td>
        <td>Treatment details:</td>
        <td colspan="2"></td>
    </tr>
    <tr>
        <td>Number of treatments: 8</td>
        <td>T1-Nutrient Expert for 8 t ha⁻¹ (150:47:59:25 kg NPKZn kg ha⁻¹)</td>
        <td colspan="2"></td>
    </tr>
    <tr>
        <td>Number of replications: 3</td>
        <td>T2-University recommendation (150:75:40:20 kg NPKZn kg ha⁻¹)</td>
        <td colspan="2"></td>
    </tr>
    <tr>
        <td>Tillage practices: 3 (Farmers' practice, zero till + mulch and zero till - mulch)</td>
        <td>T3-Farmers' practice (109:58:38:25 kg NPKZn kg ha⁻¹)</td>
        <td colspan="2"></td>
    </tr>
    <tr>
        <td>Date of sowing: 16.11.2011</td>
        <td>T4-Control (0:0:0:0 kg NPKZn kg ha⁻¹)</td>
        <td colspan="2"></td>
    </tr>
    <tr>
        <td rowspan="4"></td>
        <td>T5-SSNM for 10 t ha⁻¹ (190:64:81:25 kg NPKZn kg ha⁻¹)</td>
        <td colspan="2"></td>
    </tr>
    <tr>
        <td>T6- -N in SSNM (0:64:81:25 kg NPKZn kg ha⁻¹)</td>
        <td colspan="2"></td>
    </tr>
    <tr>
        <td>T7- -P in SSNM (190:0:81:25 kg NPKZn kg ha⁻¹)</td>
        <td colspan="2"></td>
    </tr>
    <tr>
        <td>T8- -K in SSNM (190:64:0:25 kg NPKZn kg ha⁻¹)</td>
        <td colspan="2"></td>
    </tr>
  </tbody>
</table>

**Table 1.** Characteristics of the sites for the field evaluation of Nutrient Expert® for Hybrid Maize in Indonesia and the Philippines, 2010-2011.

<table>
  <tbody>
    <tr>
        <td>Country &amp; Site No.</td>
        <td>Province</td>
        <td>District/Municipality</td>
        <td>Ecosystem†</td>
        <td>Cropping pattern</td>
        <td>Farmers</td>
    </tr>
    <tr>
        <th>Indonesia</th>
        <th colspan="5"></th>
    </tr>
    <tr>
        <td>1</td>
        <td>East Java</td>
        <td>Kediri</td>
        <td>IR</td>
        <td>Rice-rice-maize</td>
        <td>5</td>
    </tr>
    <tr>
        <td>2</td>
        <td>Lampung</td>
        <td>Punggur</td>
        <td>RF</td>
        <td>Maize-maize</td>
        <td>5</td>
    </tr>
    <tr>
        <td>3</td>
        <td>North Sumatra</td>
        <td>Langkat</td>
        <td>RF</td>
        <td>Maize-maize</td>
        <td>5</td>
    </tr>
    <tr>
        <td>4</td>
        <td>North Sumatra</td>
        <td>Langkat</td>
        <td>IR</td>
        <td>Rice-rice-maize</td>
        <td>4</td>
    </tr>
    <tr>
        <td>5</td>
        <td>South Sulawesi</td>
        <td>Bone</td>
        <td>RF</td>
        <td>Maize-maize</td>
        <td>3</td>
    </tr>
    <tr>
        <th>Philippines</th>
        <th colspan="5"></th>
    </tr>
    <tr>
        <td>1</td>
        <td>Pangasinan</td>
        <td>Bayambang</td>
        <td>RFSI</td>
        <td>Rice-maize</td>
        <td>5</td>
    </tr>
    <tr>
        <td>2</td>
        <td>Laguna</td>
        <td>Calamba</td>
        <td>RF</td>
        <td>Maize-maize</td>
        <td>3</td>
    </tr>
    <tr>
        <td>3</td>
        <td>Occidental Mindoro</td>
        <td>Abra de Ilog</td>
        <td>RFSI</td>
        <td>Rice-maize</td>
        <td>4</td>
    </tr>
    <tr>
        <td>4</td>
        <td>Iloilo</td>
        <td>Cabatuan</td>
        <td>RF</td>
        <td>Maize-maize</td>
        <td>6</td>
    </tr>
    <tr>
        <td>5</td>
        <td>Negros Occidental</td>
        <td>Murcia</td>
        <td>RF</td>
        <td>Maize-maize</td>
        <td>7</td>
    </tr>
    <tr>
        <td>6</td>
        <td>Davao</td>
        <td>Tugbok</td>
        <td>RF</td>
        <td>Maize-maize</td>
        <td>2</td>
    </tr>
    <tr>
        <td>7</td>
        <td>Maguindanao</td>
        <td>Datu Odin Sinsuat, Sultan Mastura, Ampatuan, Sultan Kudarat</td>
        <td>RF</td>
        <td>Maize-maize</td>
        <td>4</td>
    </tr>
  </tbody>
</table>
† IR = irrigated, RF = fully rainfed, RFSI = rainfed with supplemental irrigation.

**Table 2.** Agronomic and economic performance of Nutrient Expert® for Hybrid Maize at five sites (3 to 5 farmers per site) in Indonesia and seven sites (2 to 7 farmers per site) in the Philippines, 2010–2011.

<table>
  <thead>
    <tr>
        <th rowspan="2">Parameter</th>
        <th colspan="3">- - - - - - - - Indonesia (n = 22) - - - - - - - -</th>
        <th colspan="3">- - - - - - - - Philippines (n = 31) - - - - - - - -</th>
    </tr>
    <tr>
        <th>FFP</th>
        <th>NE</th>
        <th>(NE – FFP)†</th>
        <th>FFP</th>
        <th>NE</th>
        <th>(NE – FFP)†</th>
    </tr>
  </thead>
  <tbody>
    <tr>
        <td>Grain yield, t/ha</td>
        <td>7.5</td>
        <td>8.4</td>
        <td>+0.9 ***</td>
        <td>7.5</td>
        <td>9.1</td>
        <td>+1.6 ***</td>
    </tr>
    <tr>
        <td>Fertiliser N, kg/ha</td>
        <td>173</td>
        <td>160</td>
        <td>-12 ns</td>
        <td>107</td>
        <td>132</td>
        <td>+25 **</td>
    </tr>
    <tr>
        <td>Fertiliser P, kg/ha</td>
        <td>19</td>
        <td>14</td>
        <td>-4 *</td>
        <td>12</td>
        <td>15</td>
        <td>+4 **</td>
    </tr>
    <tr>
        <td>Fertiliser K, kg/ha</td>
        <td>23</td>
        <td>34</td>
        <td>+11 **</td>
        <td>18</td>
        <td>29</td>
        <td>+11 **</td>
    </tr>
    <tr>
        <td>Fertiliser cost, US$/ha</td>
        <td>126</td>
        <td>126</td>
        <td>0 ns</td>
        <td>176</td>
        <td>240</td>
        <td>+64 ***</td>
    </tr>
    <tr>
        <td>GRF‡, US$/ha</td>
        <td>1,761</td>
        <td>2,032</td>
        <td>+271 ***</td>
        <td>1,738</td>
        <td>2,117</td>
        <td>+379 ***</td>
    </tr>
  </tbody>
</table>
\*\*\*, \*\*, \*: significant at 0.001, 0.01 and 0.05 level respectively; ns = not significant
† Statistical analysis was performed with JMP version 8 (SAS Institute, 2009) using Mixed Procedure with sites as random effects.
‡GRF refers to the gross return above seed and fertiliser costs; estimated using actual local prices of seed, fertiliser and maize grain at US$1 = IDR 8,850 (Indonesia), Php 43 (Philippines).

Nutrient Expert® estimates the attainable yield and yield response to fertiliser from site information using decision rules developed from on-farm trials. It uses:

(a) Characteristics of the growing environment like water availability (irrigated, fully rainfed, rainfed with supplemental irrigation) and any occurrence of yield-limiting constraints such as flooding, drought etc.;
(b) Soil fertility indicators like soil texture, soil color and organic matter content, soil test for P or K (if any), historical use of organic materials (if any), problem soils (if any);
(c) Crop sequence in the farmer's cropping pattern;
(d) Crop residue management and fertiliser inputs; and
(e) Farmers' current yields.

The development of NE is done through collaboration with crop advisors from both public and private sectors, as well as with scientists and extension specialists to ensure that NE meets users' needs and preferences, thereby increasing the likelihood of its adoption. Collaboration is carried out through a series of dialogues, consultations and partnerships towards (a) collection of locally-available agronomic data and information, (b) integration of local user's preferences such as use of local language, measurement units, locally-available fertiliser sources, etc. and (c) field testing, evaluation and refinement of the NE software.

### Nutrient Expert® for Hybrid Maize
As NE can be applied to any cereal crop, the NE for Hybrid Maize (NEHM) was developed for favorable, tropical rainfed

and irrigated environments. It was designed to ask simple questions, which can be answered from existing information for a field or recommendation domain. The questions were grouped into five modules, viz., (1) current practice, (2) planting density, (3) SSNM rates, (4) sources and splitting and (5) profit analysis. The first three modules include questions that determine attainable yield and yield responses to fertiliser. The SSNM rates module provides N, P and K requirements for the selected attainable yield.

Consistent with SSNM, which promotes the 4Rs of nutrient stewardship (right source, right rate, right time and right place), NEHM specifies the amount and timing of fertiliser to apply, including split applications. In the sources and splitting module, NEHM recommends two or three splits for N, that all P be applied at or soon after sowing and that K be applied once or twice depending on the rate. It selects among fertilisers that the user specifies, choosing those whose nutrient contents match the requirement for optimal split dressings. It also recommends optimum plant population specifying both plant and row spacing. The sources and splitting guidelines are location-specific with each recommendation.

The SSNM strategies for maize in Southeast Asia (Witt et al., 2009) comprised the algorithm for calculating fertiliser N, P and K requirements in NEHM. These SSNM strategies are based on known attainable yield and yield responses and were developed using 2004 to 2008 data from on-farm trials with hybrid maize at 19 important sites in Indonesia, Philippines and Vietnam. It provided a range of attainable yields and yield responses to fertiliser N, P and K across diverse environments characterised by variations in amount and distribution of rainfall, varieties and crop durations, soils and cropping systems.

The NEHM model developed was validated in Indonesia and the Philippines in sites without nutrient omission trial data. Existing site and farming information were used to estimate attainable yield and expected yield responses to fertiliser and generate fertiliser recommendation for each field or location. Some users developed fertiliser guidelines for a field, using an individual farmer's data, while others used it for a recommendation domain using data from several representative farmers. The domain-level recommendations were used to develop quick guides for maize for larger geographic areas such as municipalities or districts.

The NEHM recommendations were tested in farmers' fields (plot size $\ge$ 0.1 ha) against farmer's fertiliser practice (FFP) in 2010–2011 at five sites in Indonesia (3 to 5 farmers per site) and seven sites in the Philippines (2 to 7 farmers per site) (**Table 1**). The sites included key maize production areas with maize-maize or rice-maize cropping sequence under favorable rainfed as well as irrigated environments in the two countries.

NEHM increased yield and profit of farmers in both Indonesia and the Philippines (**Table 2**). Results from 22 farmers' fields across five sites in Indonesia showed that NEHM increased yield by 0.9 t/ha, which increased the gross return over seed and fertiliser costs (GRF) by US$270/ha over FFP. Compared with FFP, NEHM recommendations reduced fertiliser P (–4 kg/ha), increased fertiliser K (+11 kg/ha) and did not significantly change fertiliser N. In the Philippines (with data from 31 fields across seven sites), NEHM increased yield by 1.6 t/ha and GRF by US$380/ha compared with FFP (**Table 2**). Compared with FFP, NEHM gave higher rates of all three nutrients (+25 kg N/ha, +4 kg P/ha and +11 kg K/ha), which substantially increased fertiliser costs (US$64/ha), but still increased profit by about six times the additional investment in fertiliser.

NEHM increased yield and economic benefits of farmers in Indonesia and the Philippines by providing a nutrient management strategy tailored to field-specific or domain-specific conditions. NEHM recommendations ensured that sufficient amount of all nutrients (N, P, K, as well as secondary and micronutrients when deficient) needed to attain the yield goal were applied at the critical growth stages of the maize crop. In Indonesia, farmers' nutrient application rates were not always less than NEHM (**Table 2**), indicating that the yield increase with NEHM could have been due to the balanced application of nutrients, as well as optimising the N splitting ratio and application timing, thus improving the efficiency of applied fertiliser nutrients. In the Philippines, the increase in yield with NEHM was largely due to the increased rates of nutrients applied at critical growth stages as compared to the farmers' nutrient rates and timing of application.

### Summary
Results of the field evaluation of NEHM in Indonesia and the Philippines demonstrated the ability of NE to increase farmer's yield and income across a range of climates, soil types and cropping systems. Nutrient Expert<sup>®</sup> provides crop advisors with a simpler and faster way to use SSNM and it enables strategic formulation of nutrient management guidelines for maize and other crops in different geographic regions and countries. Nutrient Expert<sup>®</sup> allows the determination of a range of yield goals taking into account the potential yield for the specific area, the attainable yield with optimal nutrient management as well as the farmer's objectives (food security or income) and resources. This provides added value in moving from what are now blanket recommendations to developing nutrient management recommendations that match the goals of the farmer and conditions in specific sites. BC-SA

*Dr. Pampolino is with the IPNI Southeast Asia Program; email: mpampolino@ipni.net. Dr. Witt is with the Bill and Melinda Gates Foundation, Seattle, WA. Ms. Pasuquin is with the International Rice Research Institute (IRRI), Los Baños, Philippines. Dr. Johnston is Vice-President, IPNI Asia and Africa Group, Saskatoon, Canada. Dr. Fisher is with Centro Internacional de Agricultura Tropical (CIAT), Cali, Colombia.*

### References
Buresh, R.J., M.F. Pampolino, and C. Witt. 2010. Plant & Soil 335:35-64.
Dobermann, A. and K.G. Cassman. 2002. Plant and Soil 247: 153-175.
Dobermann, A. et al. 2003. Agronomy Journal 95, 924-935.
Janssen, B.H. et al. 1990. Geoderma 46:299-318.
IRRI. 2011. http://irri.org/our-science/crop-environment/site-specific-nutrient-management.
Setiyono, T.D., D.T. Walters, K.G. Cassman, C. Witt, and A. Dobermann. 2010. Field Crops Res. 118:158-168.
Witt, C., J.M. Pasuquin, M.F. Pampolino, R.J. Buresh, and A. Dobermann. 2009. International Plant Nutrition Institute, Penang, Malaysia, http://seap.ipni.net.

# Nutrient Expert®–Maize: A Tool for Increasing Crop Yields and Farm Profit

By T. Satyanarayana, Kaushik Majumdar, Sudarshan Dutta, M.L. Jat, S.K. Pattanayak, D.P. Biradar, Y.R. Aladakatti, Mirasol Pampolino, and Adrian Johnston

**Nutrient Expert®-based fertiliser recommendations were validated and demonstrated across 191 major maize growing locations in southern India and Odisha showed an overall increase in yield by 1.1 t/ha over the current farmer fertiliser practice. It also helped in improving the profitability of maize farmers in the region. Nutrient Expert®, which follows the principles of the 4R Nutrient Stewardship approach, proved to be a boon to smallholder farmers in the region.**

Nutrient Expert® (NE), a nutrient decision support tool, is developed by the International Plant Nutrition Institute (IPNI) following the principles of 4R Nutrient Stewardship and site-specific nutrient management (SSNM). NE is an easy-to-use, interactive computer-based decision support tool that can rapidly provide nutrient recommendation for an individual farmers’ field in the presence or absence of soil testing data (Pampolino et al., 2012). It was developed in 2010-11 in collaboration with stakeholders including scientists, extension agents, and crop advisors from both government and private organisations. The NE provides crop advisors with a simple and rapid tool to apply SSNM principles in individual farmer’s fields through the use of existing site information. Besides providing location specific nutrient recommendations, the tool has options to tailor recommendations based on those resources available to the farmers.

Nutrient Expert® for hybrid maize, a MS Access-based computer application consists of five working modules. Current Nutrient Management Practice, the first module in the software documents the history of maize yields obtained in the farmers’ fields and records the corresponding extent of nutrients applied by the farmers both through organic and inorganic fertiliser sources. The Planting Density module decides whether or not the farmer is practicing an optimum plant population in his/her maize field and suggests a suitable plant population in the case of farmer’s not practicing an optimum planting density. SSNM Rates, the third and the most critical module of the software, initially establishes an attainable yield target considering the growing environment of the farmer’s field. It estimates the indigenous nutrient supplying capacity (contribution from crop residue recycling, addition of organic manures, residual benefit from the previous crop) of the farmer’s field, determines yield responses to application of major NPK nutrients and finally arrives at the most appropriate nutrient recommendation adequate for obtaining the targeted attainable yield. The Sources and Splitting module transforms the nutrient rates into fertiliser sources available at farmer’s door step and provides a final 4R compliant (i.e., Right Source, Right Rate, Right Time and Right Place) recommendation report to the farmer. The Profit Analysis module compares the cost economics associated with both the SSNM and the farmers’ practice and suggests whether or not it is profitable of practicing NE-based fertiliser recommendation.

The development and validation of NE during 2010-12, including the accumulation of promising on-farm results, led to the official launching of the NE for free public use on 20 June 2013. This paper summarises the results obtained from the on-farm validation experiments conducted in the southern region of IPNI South Asia Program and compares the performance of NE-based fertiliser recommendations over the other existing nutrient management practices. On-farm experiments evaluating the performance of NE over SR (official fertiliser recommendations by respective states) and FP (farmers’ fertiliser application practice) were conducted at 191 major maize-growing sites across Maharashtra, Andhra Pradesh, Karnataka, Tamil Nadu, and Odisha. The comparative experiments were distributed in both the *kharif* and *rabi* seasons, and were conducted in varying maize-growing environments, under rainfed and assured irrigated conditions. 

**Comparative performance** of Farmer Practice (left farmer), Nutrient Expert® (right farmer) and State Recommendation (Dr. Pattanayak standing near the SR treatment).

> **Abbreviations and notes:** N = nitrogen; P = phosphorus; K = potassium.

**Table 1.** Comparison of Nutrient Expert® (NE) estimated yield responses and the actual on-farm responses.

<table>
  <thead>
    <tr>
        <th colspan="7">- - - - - - - - - - - - - - NE-estimated response, kg/ha - - - - - - - - - - - - - -</th>
        <th colspan="6">- - - - - - - - - - - - - - Actual on-farm response, kg/ha - - - - - - - - - - - - - -</th>
    </tr>
    <tr>
        <th rowspan="2">Region</th>
        <th colspan="2">N</th>
        <th colspan="2">P₂O₅</th>
        <th colspan="2">K₂O</th>
        <th colspan="2">N</th>
        <th colspan="2">P₂O₅</th>
        <th colspan="2">K₂O</th>
    </tr>
    <tr>
        <th>Mean</th>
        <th>CV, %</th>
        <th>Mean</th>
        <th>CV, %</th>
        <th>Mean</th>
        <th>CV, %</th>
        <th>Mean</th>
        <th>CV, %</th>
        <th>Mean</th>
        <th>CV, %</th>
        <th>Mean</th>
        <th>CV, %</th>
    </tr>
  </thead>
  <tbody>
    <tr>
        <td>Andhra Pradesh</td>
        <td>5,573</td>
        <td>26</td>
        <td>1,287</td>
        <td>55</td>
        <td>260</td>
        <td>45</td>
        <td>4,351</td>
        <td>36</td>
        <td>2,730</td>
        <td>60</td>
        <td>2,023</td>
        <td>63</td>
    </tr>
    <tr>
        <td>Maharashtra</td>
        <td>4,026</td>
        <td>23</td>
        <td>1,026</td>
        <td>58</td>
        <td>1,013</td>
        <td>31</td>
        <td>4,900</td>
        <td>17</td>
        <td>1,913</td>
        <td>47</td>
        <td>900</td>
        <td>49</td>
    </tr>
    <tr>
        <td>Tamil Nadu</td>
        <td>3,500</td>
        <td>16</td>
        <td>625</td>
        <td>120</td>
        <td>500</td>
        <td>115</td>
        <td>2,433</td>
        <td>48</td>
        <td>492</td>
        <td>96</td>
        <td>447</td>
        <td>51</td>
    </tr>
    <tr>
        <td>Odisha</td>
        <td>3,484</td>
        <td>25</td>
        <td>1,081</td>
        <td>36</td>
        <td>532</td>
        <td>48</td>
        <td>3,125</td>
        <td>20</td>
        <td>2,210</td>
        <td>70</td>
        <td>1,135</td>
        <td>22</td>
    </tr>
  </tbody>
</table>

### Comparison of NE-estimated Attainable Yield and Actual Maize Yield
NE is capable of estimating the major nutrient requirement

<table>
    <tr>
        <th>Season</th>
        <th>Region</th>
        <th>Actual maize yield (t/ha)</th>
        <th>NE estimated Attainable maize yield (t/ha)</th>
    </tr>
    <tr>
        <td>Kharif</td>
        <td>Maharashtra</td>
        <td>7.9</td>
        <td>8.3</td>
    </tr>
    <tr>
        <td>Rabi</td>
        <td>Maharashtra</td>
        <td>10.2</td>
        <td>10.5</td>
    </tr>
    <tr>
        <td>Kharif</td>
        <td>Karnataka</td>
        <td>8.2</td>
        <td>8.4</td>
    </tr>
    <tr>
        <td>Rabi</td>
        <td>Karnataka</td>
        <td>10.3</td>
        <td>9.8</td>
    </tr>
    <tr>
        <td>Kharif</td>
        <td>Tamil Nadu</td>
        <td>9.1</td>
        <td>8.3</td>
    </tr>
    <tr>
        <td>Rabi</td>
        <td>Tamil Nadu</td>
        <td>6.9</td>
        <td>7.3</td>
    </tr>
    <tr>
        <td>Kharif</td>
        <td>Odisha</td>
        <td>5.4</td>
        <td>6.0</td>
    </tr>
</table>**Figure 1.** Comparison of Nutrient Expert® (NE)-estimated attainable maize yield versus actual maize yield.

for a practical and challenging yield target established by the software under the SSNM Rates module. The comparative figure (**Figure 1**) showing the NE-estimated attainable yields and the actual maize yields recorded in the farmer fields indicated that NE-based fertiliser recommendations proved to be successful in reaching the yield targets estimated by the software. The NE-estimated average attainable yield targets during the kharif season were 8.3, 8.4, 8.3, and 6.0 t/ha in the respective states of Maharashtra, Andhra Pradesh, Karnataka, Tamil Nadu and Odisha. The corresponding average actual maize yields realised in these states were 7.9, 8.2, 9.1. and 5.4 t/ha indicating that fertiliser recommendations developed using NE successfully helped in meeting the targeted attainable yields. The actual maize yields recorded in farmer fields were higher than the NE-estimated attainable yields during the

**Table 2.** Comparison of nutrient use (kg/ha) between the Nutrient Expert® (NE)-based fertiliser recommendation and Farmer's Practice (FP).

<table>
  <thead>
    <tr>
        <th rowspan="2">Parameter</th>
        <th colspan="4">Kharif (monsoon season)</th>
        <th colspan="4">Rabi (winter season)</th>
    </tr>
    <tr>
        <th>NE</th>
        <th>FP</th>
        <th>NE-FP</th>
        <th></th>
        <th>NE</th>
        <th>FP</th>
        <th>NE-FP</th>
        <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
        <td>ANDHRA PRADESH</td>
        <td colspan="4">- - - - - - - - - - - - - - - (n = 44) - - - - - - - - - - - - - - -</td>
        <td colspan="4">- - - - - - - - - - - - - - - (n = 51) - - - - - - - - - - - - - - -</td>
    </tr>
    <tr>
        <td>Fertiliser N</td>
        <td>110-190 (169)</td>
        <td>136-550 (196)</td>
        <td>-42</td>
        <td>***</td>
        <td>150-257 (211)</td>
        <td>121-534 (254)</td>
        <td>-43</td>
        <td>*</td>
    </tr>
    <tr>
        <td>Fertiliser P₂O₅</td>
        <td>17-84 (61)</td>
        <td>25-230 (123)</td>
        <td>-62</td>
        <td>**</td>
        <td>27-92 (55)</td>
        <td>21-79 (48)</td>
        <td>7</td>
        <td>***</td>
    </tr>
    <tr>
        <td>Fertiliser K₂O</td>
        <td>18-143 (87)</td>
        <td>38-150 (80)</td>
        <td>7</td>
        <td>ns</td>
        <td>25-105 (70)</td>
        <td>0-168 (64)</td>
        <td>6</td>
        <td>ns</td>
    </tr>
    <tr>
        <td>MAHARASHTRA</td>
        <td colspan="4">- - - - - - - - - - - - - - - (n = 27) - - - - - - - - - - - - - - -</td>
        <td colspan="4">- - - - - - - - - - - - - - - (n = 11) - - - - - - - - - - - - - - -</td>
    </tr>
    <tr>
        <td>Fertiliser N</td>
        <td>106-185 (152)</td>
        <td>80-191 (135)</td>
        <td>17</td>
        <td>ns</td>
        <td>110-190 (154)</td>
        <td>80-218 (130)</td>
        <td>24</td>
        <td>ns</td>
    </tr>
    <tr>
        <td>Fertiliser P₂O₅</td>
        <td>20-81 (46)</td>
        <td>46-138 (85)</td>
        <td>-39</td>
        <td>***</td>
        <td>17-64 (42)</td>
        <td>58-115 (77)</td>
        <td>-35</td>
        <td>***</td>
    </tr>
    <tr>
        <td>Fertiliser K₂O</td>
        <td>22-104 (66)</td>
        <td>0-110 (59)</td>
        <td>7</td>
        <td>ns</td>
        <td>29-81 (57)</td>
        <td>0-75 (29)</td>
        <td>28</td>
        <td>*</td>
    </tr>
    <tr>
        <td>TAMIL NADU</td>
        <td colspan="4">- - - - - - - - - - - - - - - (n = 12) - - - - - - - - - - - - - - -</td>
        <td colspan="4">- - - - - - - - - - - - - - - (n = 12) - - - - - - - - - - - - - - -</td>
    </tr>
    <tr>
        <td>Fertiliser N</td>
        <td>130-210 (182)</td>
        <td>147-332 (225)</td>
        <td>-43</td>
        <td>*</td>
        <td>130-150 (148)</td>
        <td>95-360 (210)</td>
        <td>-62</td>
        <td>*</td>
    </tr>
    <tr>
        <td>Fertiliser P₂O₅</td>
        <td>27-47 (42)</td>
        <td>48-79 (67)</td>
        <td>-25</td>
        <td>***</td>
        <td>28-47 (39)</td>
        <td>25-258 (111)</td>
        <td>-72</td>
        <td>*</td>
    </tr>
    <tr>
        <td>Fertiliser K₂O</td>
        <td>29-55 (43)</td>
        <td>48-352 (201)</td>
        <td>-158</td>
        <td>***</td>
        <td>22-59 (31)</td>
        <td>50-270 (128)</td>
        <td>-97</td>
        <td>**</td>
    </tr>
    <tr>
        <td>ODISHA</td>
        <td colspan="4">- - - - - - - - - - - - - - - (n = 34) - - - - - - - - - - - - - - -</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
    <tr>
        <td>Fertiliser N</td>
        <td>110-170 (141)</td>
        <td>27-367 (103)</td>
        <td>38</td>
        <td>***</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
    <tr>
        <td>Fertiliser P₂O₅</td>
        <td>18-67 (41)</td>
        <td>20-115 (52)</td>
        <td>-11</td>
        <td>ns</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
    <tr>
        <td>Fertiliser K₂O</td>
        <td>21-104 (46)</td>
        <td>0-192 (59)</td>
        <td>-13</td>
        <td>ns</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
  </tbody>
</table>
***, ** and * significant at p < 0.001, 0.01 and 0.05 levels; ns = non-significant. NE, FP and SR = Nutrient Expert®, Farmer Practice and State Recommendation. Values in parenthesis represent mean values.

**Table 3.** Performance of Nutrient Expert® (NE)-based recommendations for yield and economics of maize in southern region.

<table>
  <thead>
    <tr>
        <th>Parameter</th>
        <th>Unit</th>
        <th colspan="5">- - - - - - - - - - - - Kharif (monsoon season) - - - - - - - - - - - -</th>
        <th colspan="5">- - - - - - - - - - - - - - - Rabi (winter season) - - - - - - - - - - - - - - -</th>
        <th colspan="4"></th>
    </tr>
    <tr>
        <th></th>
        <th></th>
        <th>NE</th>
        <th>FP</th>
        <th>SR</th>
        <th>NE-FP</th>
        <th>NE-SR</th>
        <th>NE</th>
        <th>FP</th>
        <th>SR</th>
        <th>NE-FP</th>
        <th>NE-SR</th>
        <th colspan="4"></th>
    </tr>
    <tr>
        <th colspan="2">ANDHRA PRADESH (n = 95)</th>
        <th colspan="5">- - - - - - - - - - - - - - - - - - (n = 44) - - - - - - - - - - - - - - - - - - - - -</th>
        <th colspan="5">- - - - - - - - - - - - - - - - - - (n = 51) - - - - - - - - - - - - - - - - - - - - -</th>
        <th colspan="4"></th>
    </tr>
  </thead>
  <tbody>
    <tr>
        <td>Grain Yield</td>
        <td>kg/ha</td>
        <td>7,943</td>
        <td>6,525</td>
        <td>7,297</td>
        <td>1,418</td>
        <td>***</td>
        <td>646</td>
        <td>ns</td>
        <td>9,736</td>
        <td>8,689</td>
        <td>8,813</td>
        <td>1,047</td>
        <td>***</td>
        <td>923</td>
        <td>***</td>
    </tr>
    <tr>
        <td>Fertiliser Cost</td>
        <td>₹/ha</td>
        <td>5,398</td>
        <td>5,996</td>
        <td>4,991</td>
        <td>-598</td>
        <td>ns</td>
        <td>407</td>
        <td>***</td>
        <td>5,515</td>
        <td>7,740</td>
        <td>5,220</td>
        <td>-2,225</td>
        <td>***</td>
        <td>295</td>
        <td>ns</td>
    </tr>
    <tr>
        <td>GRF</td>
        <td>₹/ha</td>
        <td>74,032</td>
        <td>59,254</td>
        <td>67,979</td>
        <td>14,778</td>
        <td>***</td>
        <td>6,053</td>
        <td>***</td>
        <td>91,845</td>
        <td>79,150</td>
        <td>82,910</td>
        <td>12,695</td>
        <td>***</td>
        <td>8,935</td>
        <td>***</td>
    </tr>
    <tr>
        <th colspan="2">MAHARASHTRA (n = 38)</th>
        <th colspan="5">- - - - - - - - - - - - - - - - - - (n = 27) - - - - - - - - - - - - - - - - - - - - -</th>
        <th colspan="5">- - - - - - - - - - - - - - - - - - (n = 11) - - - - - - - - - - - - - - - - - - - - -</th>
        <th colspan="4"></th>
    </tr>
    <tr>
        <td>Grain Yield</td>
        <td>kg/ha</td>
        <td>8,153</td>
        <td>7,591</td>
        <td>7,033</td>
        <td>562</td>
        <td>ns</td>
        <td>1,120</td>
        <td>**</td>
        <td>10,214</td>
        <td>8,831</td>
        <td>9,835</td>
        <td>1,383</td>
        <td>***</td>
        <td>379</td>
        <td>**</td>
    </tr>
    <tr>
        <td>Fertiliser Cost</td>
        <td>₹/ha</td>
        <td>4,455</td>
        <td>5,385</td>
        <td>5,543</td>
        <td>-930</td>
        <td>**</td>
        <td>-1,088</td>
        <td>**</td>
        <td>4,943</td>
        <td>4,481</td>
        <td>5,543</td>
        <td>462</td>
        <td>ns</td>
        <td>-600</td>
        <td>***</td>
    </tr>
    <tr>
        <td>GRF</td>
        <td>₹/ha</td>
        <td>77,075</td>
        <td>70,525</td>
        <td>64,787</td>
        <td>6,550</td>
        <td></td>
        <td>12,288</td>
        <td></td>
        <td>97,197</td>
        <td>83,829</td>
        <td>92,807</td>
        <td>13,368</td>
        <td></td>
        <td>4,390</td>
        <td></td>
    </tr>
    <tr>
        <th colspan="2">TAMIL NADU (n = 24)</th>
        <th colspan="5">- - - - - - - - - - - - - - - - - - (n = 12) - - - - - - - - - - - - - - - - - - - - -</th>
        <th colspan="5">- - - - - - - - - - - - - - - - - - (n = 12) - - - - - - - - - - - - - - - - - - - - -</th>
        <th colspan="4"></th>
    </tr>
    <tr>
        <td>Grain Yield</td>
        <td>kg/ha</td>
        <td>8,774</td>
        <td>8,154</td>
        <td>7,622</td>
        <td>620</td>
        <td>**</td>
        <td>1,152</td>
        <td>ns</td>
        <td>7,405</td>
        <td>6,550</td>
        <td>7,114</td>
        <td>855</td>
        <td>***</td>
        <td>291</td>
        <td>ns</td>
    </tr>
    <tr>
        <td>Fertiliser Cost</td>
        <td>₹/ha</td>
        <td>4,232</td>
        <td>8,488</td>
        <td>4,514</td>
        <td>-4,256</td>
        <td>***</td>
        <td>-282</td>
        <td>***</td>
        <td>3,546</td>
        <td>8,395</td>
        <td>5,960</td>
        <td>-4,849</td>
        <td>**</td>
        <td>-2,414</td>
        <td>***</td>
    </tr>
    <tr>
        <td>GRF</td>
        <td>₹/ha</td>
        <td>83,230</td>
        <td>73,058</td>
        <td>71,988</td>
        <td>10,172</td>
        <td>***</td>
        <td>11,242</td>
        <td>ns</td>
        <td>68,099</td>
        <td>57,106</td>
        <td>67,595</td>
        <td>10,993</td>
        <td>***</td>
        <td>504</td>
        <td>ns</td>
    </tr>
    <tr>
        <th colspan="2">ODISHA (n = 34)</th>
        <th colspan="5">- - - - - - - - - - - - - - - - - - (n = 34) - - - - - - - - - - - - - - - - - - - - -</th>
        <th colspan="5">-</th>
        <th colspan="4"></th>
    </tr>
    <tr>
        <td>Grain Yield</td>
        <td>kg/ha</td>
        <td>5,394</td>
        <td>3,611</td>
        <td>4,334</td>
        <td>1,783</td>
        <td>***</td>
        <td>1,060</td>
        <td>***</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
    <tr>
        <td>Fertiliser Cost</td>
        <td>₹/ha</td>
        <td>3,445</td>
        <td>4,264</td>
        <td>2,638</td>
        <td>819</td>
        <td>ns</td>
        <td>807</td>
        <td>***</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
    <tr>
        <td>GRF</td>
        <td>₹/ha</td>
        <td>50,495</td>
        <td>31,846</td>
        <td>40,702</td>
        <td>18,649</td>
        <td>***</td>
        <td>9,793</td>
        <td>***</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
  </tbody>
</table>
***, ** and * significant at p < 0.001, 0.01 and 0.05 levels; ns = non-significant. GRF = gross return above fertiliser cost.

kharif season in Tamil Nadu. Similar observations were also noticed during the rabi season in MAHARASHTRA. NE estimates the attainable yield targets based on robust scientific principles, considers growing environment according to site characteristics and farmers’ actual yield while estimating the realistic attainable yield.

### Comparison of NE-estimated Yield Responses versus Actual Yield Responses

Yield response to fertiliser application is a function of indigenous nutrient supplying capacity of soil and is determined from soil characteristics (i.e., texture, colour and content of organic matter), historical use of organic inputs (if any), and apparent nutrient balance (for P and K) from the previous crop. The algorithms involved in NE are so rigorous that it captures the required information through logical questions and estimates the yield responses close to the actual yield responses determined through omission plot techniques. The NE-estimated yield responses compared with that of actual yield responses (**Table 1**) showed that N responses estimated with NE were higher by 28, 44 and 11% in Andhra Pradesh, Tamil Nadu and Odisha and lesser by 18% in MAHARASHTRA than the actual N response. The NE-estimated P response was higher than the actual P response in Tamil Nadu by 27% and NE-estimated K response was higher than the actual K response in MAHARASHTRA and Tamil Nadu by 13 and 12%. In the rest of the regions, NE estimated lower P and K responses than the actual response. Averaged over four states, NE estimated 16% higher N response, 31% lower P<sub>2</sub>O<sub>5</sub> response and 29% lower K<sub>2</sub>O response over the actual responses observed through omission plot techniques (**Table 1**). The variation in yield response estimated with NE over the actual yield response observed from limited number of omission plot experiments indicated that NE is capable of capturing the temporal variability of nutrient requirement across the seasons along with considering the spatial variability between farmers’ fields. Also, NE estimates yield responses based on sound scientific principles even in the absence of soil testing and forms the basis for generating fertiliser recommendations.

### Comparison of NE-based Nutrient Recommendation with Farmer Practice

A comparative study of nutrient use between the two nutrient management options (NE and FP) was shown in **Table 2**. During kharif, NE-recommended nutrient use averaged over four states indicated that N, P<sub>2</sub>O<sub>5</sub> and K<sub>2</sub>O use with NE varied from 106 to 210, 17 to 84, and 18 to 143 kg/ha, with an average of 161, 48, and 61 kg/ha, respectively. The corresponding nutrient use based on FP varied from 136 to 550, 20 to 230, and 0 to 352 kg/ha, with an average of 169, 82, and 100 kg/ha for N, P<sub>2</sub>O<sub>5</sub> and K<sub>2</sub>O, respectively. On average, the NE-based fertiliser recommendation reduced N, P<sub>2</sub>O<sub>5</sub> and K<sub>2</sub>O use by 8, 34 and 39 kg/ha indicating 5, 40 and 39% reductions in nutrient use over FP. With the use of NE-based fertiliser recommendation, the lowest N use in FP has increased from 27 to 110 kg/ha in NE, whereas, the maximum N use in FP has decreased from 550 to 210 kg/ha in the NE-based recommendations. This indicates that NE, in addition to suggesting a right rate of nutrients sufficient to meet the attainable yield targets, also helps in optimising nutrient use through appropriate adjustments (increase or decrease) in fertiliser application. Similar observations were also noted for optimising P<sub>2</sub>O<sub>5</sub> and K<sub>2</sub>O use with NE-based fertiliser recommendations (**Table 2**). The difference between NE and FP for N and P<sub>2</sub>O<sub>5</sub> use in Andhra Pradesh, P<sub>2</sub>O<sub>5</sub> use in Maharashtra, NPK use in Tamil Nadu and N use in Odisha were statistically significant.

The fertiliser application based on NE recommendation during rabi revealed that application of N, P<sub>2</sub>O<sub>5</sub> and K<sub>2</sub>O across three southern states varied from 110 to 257, 17 to 92, and 22 to 105 kg/ha with an average of 171, 45, and 53 kg/

Odisha farmers expressed satisfaction after visiting the Nutrient Expert® plot.

ha, respectively (**Table 2**). Across all sites, on average, NE reduced N, P<sub>2</sub>O<sub>5</sub> and K<sub>2</sub>O rates by 27, 33, and 21 kg/ha over FP, resulting in a rate reduction of 14, 40, and 20% of N, P<sub>2</sub>O<sub>5</sub> and K<sub>2</sub>O use, respectively. NE recommended slightly higher N rates and slightly lower P<sub>2</sub>O<sub>5</sub> and K<sub>2</sub>O rates during rabi in comparison to the kharif. Nutrient rates generated through NE are based on the estimated yield response to NPK application and NE estimated relatively high N response in rabi season over the kharif season (data not shown). The mean yield response to application of N, P<sub>2</sub>O<sub>5</sub> and K<sub>2</sub>O during kharif were 3.9, 1.1 and 1 t/ha; whereas, the estimated responses during rabi were 5.2, 0.9 and 1 t/ha, respectively.

## NE Use and Improved Yield and Economics of Maize

Data showing the relative performance of NE use over SR and FP for grain yield of maize, fertiliser cost and GRF are given in **Table 3**. Across all sites (n = 117) during the kharif season, NE-based fertiliser use resulted in increased maize yield and economic benefit (i.e., gross return above fertiliser cost or GRF) over FP and SR. Compared to FP, on average it increased yield by 1.1 t/ha and GRF by ₹12,537/ha with a reduction in fertiliser cost (significant only at Maharashtra and Tamil Nadu) of ₹1,241/ha. NE-based fertiliser recommendations also increased yield (by 0.9 t/ha) and GRF (by ₹9,844/ha) over SR with a minimal reduction in fertiliser cost (₹-156/ha). NE-based fertiliser recommendations were also tested against FP and SR during the two consecutive rabi seasons (2011-13) at 74 locations in three southern states of Andhra Pradesh, Maharashtra and Tamil Nadu. Results revealed that across the three states, grain yield with NE significantly increased by 14 and 6% over FP and SR, respectively (**Table 3**). NE-maize also increased GRF by ₹12,352 and ₹4,430/ha over FP and SR and it reduced the fertiliser cost by ₹2,204 and ₹906/ha over FP and SR, respectively.

Improved maize yields with the use of NE-based fertiliser recommendations could be attributed to the 4R compliant scientific nutrient prescriptions generated by NE, which primarily suggests application of major NPK nutrients using the right fertiliser sources, applied at the right rate and at the right time. NE also suggested application of secondary and micronutrients wherever they were deficient (data not shown) and helped in promoting balanced use of all the essential nutrients in addition to improving yields and optimizing nutrient use. The higher GRF with the use of NE over FP and SR could be attributed to higher maize yields and the associated reduction in fertiliser cost observed with NE-based recommendations. NE provides nutrient recommendations tailored to location-specific conditions. In contrast to SR, which gives one recommendation per state (e.g., 150 kg N, 75 kg P<sub>2</sub>O<sub>5</sub>, and 75 kg K<sub>2</sub>O/ha in Andhra Pradesh), NE recommends a range of N, P<sub>2</sub>O<sub>5</sub> and K<sub>2</sub>O application rates within a region depending on attainable yield and expected responses to fertiliser at an individual farmer's field. Thus, fertiliser N, P<sub>2</sub>O<sub>5</sub> and K<sub>2</sub>O requirements determined by NE, varied among fields or locations, proved to be critical in improving the yield and economics of maize farmers in the region. In effect, use of the NE actually increased yields and profit, while reducing economic risk to the farmers, simply by providing scientific direction in the most appropriate use of fertilisers with each individual field.


Wheat yields were significantly (p ≤ 0.01) higher in NE1 compared to NE2 under both CT and ZT suggesting that an extra split of N helped increase grain yield. Applying N in wheat through three splits (33:33:33) or by two splits (50:50) are common practices among farmers in India. Often the three-split option produces better yields as applications are better matched with high physiological demand stages of the crop (Singh et al., 2002). On the other hand, the two-split option helps save labour cost of applying an extra split, which can be substantial in relatively large fields. However, generally it is observed that two-splits works equally well as three-splits in heavy soils, while three-splits produce better yields in lighter soils (Singh et al., 2002). It is likely that the abrupt increase in wheat yields (**Figure 2**) in the NE1 treatment over all other

**Figure 1.** Grain yield of wheat across different nutrient management and tillage practices. Yield with different letters are significantly (p ≤ 0.01) different.

<table>
  <thead>
    <tr>
        <th>Treatments</th>
        <th>CT 2010-11</th>
        <th>ZT 2010-11</th>
        <th>CT 2011-12</th>
        <th>ZT 2011-12</th>
    </tr>
  </thead>
  <tbody>
    <tr>
        <td>FFP</td>
        <td>4.8 (a)</td>
        <td>5.0 (a)</td>
        <td>4.8 (a)</td>
        <td>5.0 (a)</td>
    </tr>
    <tr>
        <td>SR</td>
        <td>5.2 (b)</td>
        <td>5.3 (b)</td>
        <td>5.2 (b)</td>
        <td>5.3 (b)</td>
    </tr>
    <tr>
        <td>NE1</td>
        <td>5.6 (c)</td>
        <td>5.8 (d)</td>
        <td>5.6 (c)</td>
        <td>5.8 (d)</td>
    </tr>
    <tr>
        <td>NE2</td>
        <td>5.4 (b)</td>
        <td>5.5 (c)</td>
        <td>5.4 (b)</td>
        <td>5.5 (c)</td>
    </tr>
  </tbody>
</table>
*(Note: Values in the table are estimated from the bar chart in Figure 1. Letters in parentheses represent significance groups as indicated in the original chart.)*

<table>
  <thead>
    <tr>
        <th colspan="4">Yield, kg/ha</th>
        <th></th>
    </tr>
    <tr>
        <th>Locations and years</th>
        <th>FFP</th>
        <th>SR</th>
        <th>NE1</th>
        <th>NE2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
        <td>Bihar 2010-11</td>
        <td>3.3<sup>a</sup></td>
        <td>3.7<sup>b</sup></td>
        <td>3.7<sup>b</sup></td>
        <td>3.9<sup>c</sup></td>
    </tr>
    <tr>
        <td>Bihar 2011-12</td>
        <td>5.1<sup>a</sup></td>
        <td>5.1<sup>a</sup></td>
        <td>5.4<sup>b</sup></td>
        <td>5.7<sup>c</sup></td>
    </tr>
    <tr>
        <td>Haryana 2010-11</td>
        <td>4.3<sup>a</sup></td>
        <td>4.6<sup>b</sup></td>
        <td>4.7<sup>b</sup></td>
        <td>5.2<sup>c</sup></td>
    </tr>
    <tr>
        <td>Haryana 2011-12</td>
        <td>5.0<sup>a</sup></td>
        <td>5.6<sup>b</sup></td>
        <td>5.9<sup>c</sup></td>
        <td>5.9<sup>c</sup></td>
    </tr>
    <tr>
        <td>Punjab 2010-11</td>
        <td>4.4<sup>a</sup></td>
        <td>5.0<sup>b</sup></td>
        <td>6.9<sup>c</sup></td>
        <td>4.8<sup>b</sup></td>
    </tr>
    <tr>
        <td>Punjab 2011-12</td>
        <td>4.9<sup>a</sup></td>
        <td>5.4<sup>b</sup></td>
        <td>5.8<sup>c</sup></td>
        <td>5.4<sup>b</sup></td>
    </tr>
  </tbody>
</table>

**Figure 2.** Grain yield of wheat across different nutrient management practices across different states. Yield with different letters are significantly (p ≤ 0.01) different.

treatments might be due to the light texture of the soils where trials were set up.

While considering the performance of NE across different states, the present study also highlights that both NE1 and NE2 have significantly (p ≤ 0.05) higher grain yield across the treatments in all the three study states (**Figure 2**). This suggests that nutrient recommendations from NE, generated through proper assessment of growing environment and target yields, were more suitable than generalised state recommendations or practices by farmers based on their perception. Better performance of the NE recommendations over the other practices across a large area in the Indo-Gangetic Plains (IGP) also establishes the efficacy of the tool.

We looked at the difference in nutrient application under different treatments in the three states over two seasons (**Table 1**). In the case of Bihar, N application rates did not differ among the treatments in 2010-11 but FFP rates were higher in 2011-12 than the other treatments. The P<sub>2</sub>O<sub>5</sub> application rates were lowest in NE in 2010-11, while there was no significant difference among the treatments in 2011-12. The K<sub>2</sub>O application rates were significantly higher with NE than FFP and SR in both the years. In general, nutrient application rates in FFP and NE were comparatively higher in 2011-12 and **Figure 2** shows that yield levels were higher that year than the previous wheat season.

The N application rates in Haryana in 2010-11 were the same for NE and FFP, which were both lower than SR. In 2011-12, however, the NE tool recommended less N than SR or FFP. For P<sub>2</sub>O<sub>5</sub>, application rates recommended by NE were lower than FFP and SR but the trend reversed in 2011-12 and NE recommended more P than SR and FFP. The K<sub>2</sub>O recommendations by NE were higher than FFP and SR in both the years.

The NE tool recommended higher N, P<sub>2</sub>O<sub>5</sub> and K<sub>2</sub>O than FFP and SR in Punjab in 2010-11. The NE and SR recommended similar rates of N, which was lower than FFP, and P<sub>2</sub>O<sub>5</sub> application rate remained the same for all the treatments in 2011-12. Potassium application rates were higher in NE. It is evident that NE recommendations were different in both the years and across states. This suggests that the tool-based recommendations are addressing the spatial, as well as temporal variability, reflecting the farm-to-farm changes in management.

Overall, the N application rates in the FFP treatment were significantly higher than the other treatments across tillage and years (**Figure 3**). The N doses in NE were at par with SR. The P<sub>2</sub>O<sub>5</sub> application rates were significantly (p ≤ 0.05) higher in NE as compared to FFP and SR under both the tillage practices and year (**Figure 4**). The K<sub>2</sub>O applications were significantly (p ≤ 0.05) increased in NE1 and NE2 over FFP and SR at both CT and ZT (**Figure 5**). Farmers in Punjab, Haryana and Bihar generally neglect K application in wheat. Potassium application in rice-wheat system, that is prevalent

**Table 1.** Fertiliser rates across three different states. Within states dose followed by different letters in superscript are significantly (p ≤ 0.05) different.

<table>
  <thead>
    <tr>
        <th rowspan="2">Year</th>
        <th rowspan="2">State</th>
        <th rowspan="2">Treatments</th>
        <th colspan="3">------ Rates, kg/ha ------</th>
    </tr>
    <tr>
        <th></th>
        <th></th>
        <th>N</th>
        <th>P<sub>2</sub>O<sub>5</sub></th>
        <th>K<sub>2</sub>O</th>
    </tr>
  </thead>
  <tbody>
    <tr>
        <td rowspan="12">2010-11</td>
        <td rowspan="4">Bihar</td>
        <td>FFP</td>
        <td>124<sup>a</sup></td>
        <td>48<sup>a</sup></td>
        <td>34<sup>a</sup></td>
    </tr>
    <tr>
        <td></td>
        <td>SR</td>
        <td>120<sup>a</sup></td>
        <td>60<sup>b</sup></td>
        <td>40<sup>b</sup></td>
    </tr>
    <tr>
        <td></td>
        <td>NE1</td>
        <td>115<sup>a</sup></td>
        <td>41<sup>c</sup></td>
        <td>57<sup>c</sup></td>
    </tr>
    <tr>
        <td></td>
        <td>NE2</td>
        <td>115<sup>a</sup></td>
        <td>41<sup>c</sup></td>
        <td>57<sup>c</sup></td>
    </tr>
    <tr>
        <td rowspan="4">Haryana</td>
        <td>FFP</td>
        <td>166<sup>a</sup></td>
        <td>58<sup>a</sup></td>
        <td>0<sup>a</sup></td>
    </tr>
    <tr>
        <td></td>
        <td>SR</td>
        <td>150<sup>b</sup></td>
        <td>60<sup>b</sup></td>
        <td>60<sup>b</sup></td>
    </tr>
    <tr>
        <td></td>
        <td>NE1</td>
        <td>170<sup>a</sup></td>
        <td>43<sup>c</sup></td>
        <td>81<sup>c</sup></td>
    </tr>
    <tr>
        <td></td>
        <td>NE2</td>
        <td>168<sup>a</sup></td>
        <td>45<sup>c</sup></td>
        <td>76<sup>d</sup></td>
    </tr>
    <tr>
        <td rowspan="4">Punjab</td>
        <td>FFP</td>
        <td>144<sup>a</sup></td>
        <td>53<sup>a</sup></td>
        <td>3<sup>a</sup></td>
    </tr>
    <tr>
        <td></td>
        <td>SR</td>
        <td>125<sup>b</sup></td>
        <td>62<sup>b</sup></td>
        <td>30<sup>b</sup></td>
    </tr>
    <tr>
        <td></td>
        <td>NE1</td>
        <td>158<sup>c</sup></td>
        <td>71<sup>c</sup></td>
        <td>87<sup>c</sup></td>
    </tr>
    <tr>
        <td></td>
        <td>NE2</td>
        <td>158<sup>c</sup></td>
        <td>71<sup>c</sup></td>
        <td>87<sup>c</sup></td>
    </tr>
    <tr>
        <td rowspan="12">2011-12</td>
        <td rowspan="4">Bihar</td>
        <td>FFP</td>
        <td>142<sup>a</sup></td>
        <td>64<sup>a</sup></td>
        <td>33<sup>a</sup></td>
    </tr>
    <tr>
        <td></td>
        <td>SR</td>
        <td>120<sup>b</sup></td>
        <td>60<sup>a</sup></td>
        <td>40<sup>b</sup></td>
    </tr>
    <tr>
        <td></td>
        <td>NE1</td>
        <td>128<sup>b</sup></td>
        <td>64<sup>a</sup></td>
        <td>78<sup>c</sup></td>
    </tr>
    <tr>
        <td></td>
        <td>NE2</td>
        <td>128<sup>b</sup></td>
        <td>64<sup>a</sup></td>
        <td>78<sup>c</sup></td>
    </tr>
    <tr>
        <td rowspan="4">Haryana</td>
        <td>FFP</td>
        <td>174<sup>a</sup></td>
        <td>58<sup>a</sup></td>
        <td>2<sup>a</sup></td>
    </tr>
    <tr>
        <td></td>
        <td>SR</td>
        <td>150<sup>b</sup></td>
        <td>60<sup>b</sup></td>
        <td>60<sup>b</sup></td>
    </tr>
    <tr>
        <td></td>
        <td>NE1</td>
        <td>140<sup>c</sup></td>
        <td>63<sup>c</sup></td>
        <td>86<sup>c</sup></td>
    </tr>
    <tr>
        <td></td>
        <td>NE2</td>
        <td>140<sup>c</sup></td>
        <td>63<sup>c</sup></td>
        <td>85<sup>c</sup></td>
    </tr>
    <tr>
        <td rowspan="4">Punjab</td>
        <td>FFP</td>
        <td>142<sup>a</sup></td>
        <td>64<sup>a</sup></td>
        <td>33<sup>a</sup></td>
    </tr>
    <tr>
        <td></td>
        <td>SR</td>
        <td>120<sup>b</sup></td>
        <td>60<sup>a</sup></td>
        <td>40<sup>b</sup></td>
    </tr>
    <tr>
        <td></td>
        <td>NE1</td>
        <td>128<sup>b</sup></td>
        <td>64<sup>a</sup></td>
        <td>78<sup>c</sup></td>
    </tr>
    <tr>
        <td></td>
        <td>NE2</td>
        <td>128<sup>b</sup></td>
        <td>64<sup>a</sup></td>
        <td>78<sup>c</sup></td>
    </tr>
  </tbody>
</table>
<table>
  <thead>
    <tr>
        <th colspan="5">N consumption, kg/ha</th>
    </tr>
    <tr>
        <th>Treatments</th>
        <th>CT 2010-11</th>
        <th>ZT 2010-11</th>
        <th>CT 2011-12</th>
        <th>ZT 2011-12</th>
    </tr>
  </thead>
  <tbody>
    <tr>
        <td>FFP</td>
        <td>164<sup>a</sup></td>
        <td>168<sup>a</sup></td>
        <td>165<sup>a</sup></td>
        <td>168<sup>a</sup></td>
    </tr>
    <tr>
        <td>SR</td>
        <td>133<sup>b</sup></td>
        <td>140<sup>b</sup></td>
        <td>138<sup>b</sup></td>
        <td>140<sup>b</sup></td>
    </tr>
    <tr>
        <td>NE1</td>
        <td>132<sup>b</sup></td>
        <td>139<sup>b</sup></td>
        <td>134<sup>b</sup></td>
        <td>139<sup>b</sup></td>
    </tr>
    <tr>
        <td>NE2</td>
        <td>133<sup>b</sup></td>
        <td>139<sup>b</sup></td>
        <td>134<sup>b</sup></td>
        <td>139<sup>b</sup></td>
    </tr>
  </tbody>
</table>

**Figure 3.** Fertiliser N rates across different treatments while considering all the locations. Rates with different letters are significantly (p ≤ 0.05) different.

<table>
  <thead>
    <tr>
        <th>P₂O₅ consumption, kg/ha</th>
        <th>CT 2010-11</th>
        <th>ZT 2010-11</th>
        <th>CT 2011-12</th>
        <th>ZT 2011-12</th>
    </tr>
  </thead>
  <tbody>
    <tr>
        <td>FFP</td>
        <td>57 (a)</td>
        <td>60 (a)</td>
        <td>59 (a)</td>
        <td>60 (a)</td>
    </tr>
    <tr>
        <td>SR</td>
        <td>58 (a)</td>
        <td>60 (a)</td>
        <td>61 (b)</td>
        <td>60 (a)</td>
    </tr>
    <tr>
        <td>NE1</td>
        <td>63 (b)</td>
        <td>62 (b)</td>
        <td>63 (c)</td>
        <td>62 (b)</td>
    </tr>
    <tr>
        <td>NE2</td>
        <td>63 (b)</td>
        <td>62 (b)</td>
        <td>63 (c)</td>
        <td>62 (b)</td>
    </tr>
  </tbody>
</table>

**Figure 4.** Fertiliser P₂O₅ rates across different treatments while considering all the locations. Rates with different letters are significantly (p ≤ 0.05) different.

<table>
  <thead>
    <tr>
        <th>K₂O consumption, kg/ha</th>
        <th>CT 2010-11</th>
        <th>ZT 2010-11</th>
        <th>CT 2011-12</th>
        <th>ZT 2011-12</th>
    </tr>
  </thead>
  <tbody>
    <tr>
        <td>FFP</td>
        <td>6 (a)</td>
        <td>9 (a)</td>
        <td>7 (a)</td>
        <td>8 (a)</td>
    </tr>
    <tr>
        <td>SR</td>
        <td>40 (b)</td>
        <td>50 (b)</td>
        <td>43 (b)</td>
        <td>50 (b)</td>
    </tr>
    <tr>
        <td>NE1</td>
        <td>83 (c)</td>
        <td>81 (c)</td>
        <td>84 (c)</td>
        <td>81 (c)</td>
    </tr>
    <tr>
        <td>NE2</td>
        <td>84 (c)</td>
        <td>80 (c)</td>
        <td>84 (c)</td>
        <td>81 (c)</td>
    </tr>
  </tbody>
</table>

**Figure 5.** Fertiliser K₂O rates across different treatments while considering all the locations. Rates with different letters are significantly (p ≤ 0.05) different.

in these three states, is far below the required amount. The NE tool, while assessing the cropping system nutrient balance identified a large deficit in K application and recommended high rates to reduce the negative (input-output) K balance in the fields.

### Economics
The benefit:cost (B:C) ratios of the treatments were estimated using the cost of inputs and value of the output. The results were represented considering the B:C ratio of the FFP treatment as a unit (**Figure 6**). Both the NE treatments and the SR increased the economic benefit over FFP.

Results showed that the B:C ratio of NE1 were higher than

<table>
  <thead>
    <tr>
        <th>B:C ratio over FFP</th>
        <th>2010-11</th>
        <th>2011-12</th>
    </tr>
  </thead>
  <tbody>
    <tr>
        <td>SR</td>
        <td>3.8 (a)</td>
        <td>3.0 (a)</td>
    </tr>
    <tr>
        <td>NE1</td>
        <td>4.8 (b)</td>
        <td>4.9 (b)</td>
    </tr>
    <tr>
        <td>NE2</td>
        <td>4.0 (a)</td>
        <td>3.6 (a)</td>
    </tr>
  </tbody>
</table>

**Figure 6.** Benefit:Cost ratio over FFP. Ratio with different letters is significantly (p ≤ 0.05) different. Cost of N: ₹12/kg (on the basis of Urea); Cost of P₂O₅: ₹45/kg (on the basis of single superphosphate); Cost of K₂O: ₹27/kg (on the basis of potassium chloride); Value of maize grain: ₹11/kg.

that of SR and NE2 in both 2010-11 and 2011-12 cropping years (**Figure 6**). A combination of appropriate rate estimation and better splitting of the nitrogen improved yield in the NE1 treatment over the other practices.

### Summary
NE–Wheat validation trials in the year 2010–11 and 2011–12, across three different states of the Indo-Gangetic plains, showed that the NE tool-based fertiliser recommendation increased wheat yield and economic benefit for farmers. Large-scale implementation of the tool provides the opportunity to bridge nutrient-related yield gaps in wheat and increase farm profitability in an environmentally sustainable manner. BC-SA

*Dr. Dutta (e-mail:sdutta@ipni.net), Dr. Majumdar, Dr. Shahi, Dr. Satyanarayana, and Mr. Vinod Kumar are with IPNI South Asia Program; Dr. Pampolino is with IPNI Southeast Asia Program; Dr. Jat is with CIMMYT India; Mr. Anil Kumar is with Dept. of Agriculture, Govt. of Punjab; Mr. Naveen Gupta is doctoral student at Charles Stewart University, Australia; and Dr. Johnston is IPNI Vice President and Asia & Africa Coordinator.*

### References
IRRI. 2009. In Revitalizing the Rice-Wheat Cropping Systems of the Indo-Gangetic Plains: Adaptations and Adoptions of Resource Conserving Technologies in India, Bangladesh and Nepal. International Rice Research Institute, Metro Manila, Philippines.

Pampolino, M.F., C. Witt, J.M. Pasuquin, A. Johnston, and M.J. Fisher. 2012. J. Computers and Electronics in Agri. 88:103-110.

Singh, B., Y. Singh, J.K. Ladha, K.F. Bronson, V. Balasubramanian, J. Singh and C.S. Khind. 2002. Agron. J. 94(4):821-829.