# RaceWise: Analytical Insights into F1 Racing

---

![Cover Image](https://c4.wallpaperflare.com/wallpaper/659/965/95/red-bull-f1-hd-cars-wallpaper-preview.jpg)

#### By Group15 for ECE143 at UC San Diego

#### Members:

- [Abhishikta Panja](https://github.com/AbhishiktaP)
- [Glenn Siliva](https://github.com/g-sivila)
- [Ruizhe Fan](https://github.com/cssx1234)
- [Sushaanth Srinivasan](https://github.com/SushaanthSrinivasan)
- [Taikun Lin](https://github.com/Diosssltk)

## Introduction

In Formula 1 racing, the delicate interplay between various factors can significantly influence driver performance. This data analysis project delves into the nuanced relationships that exist between age and experience, tire strategy, home advantage, gear downshifts, and weather conditions concerning driver performance. By scrutinizing these elements, we aim to unravel the intricate tapestry of influences that shape the outcome of races. Whether it's the seasoned expertise of a veteran driver, the strategic decisions made regarding tire usage, the impact of racing on home turf, the artful execution of gear downshifts, or the unpredictable dance with weather conditions, each aspect contributes to the dynamic mosaic that defines success in the high-stakes world of motorsports. Through comprehensive analysis, this project seeks to provide valuable insights into the multifaceted nature of driver performance, contributing to a deeper understanding of the sport's dynamics and potentially informing strategies for both drivers and teams alike.

## File Structure / Scripts

### To visualize all inferences:

1. Clone the repository.

```sh
git clone https://github.com/cssx1234/ECE143-Group15
```

2. Navigate into the required folder.

```sh
cd ECE143-Group15/Inferences
```

4. Install the required dependencies. \
   Example using pip:

```sh
pip install -r requirements.txt
```

5. Open the file `Visualizations.ipynb` in a Jupyter Environment, Google Colab or VS Code and run all the cells.

### To visualize individual inferences:

Included in each folder are the necessary scripts for each inference as well as README files which contain more detailed instructions and analysis.

### Age & Experience vs. Driver Performance

_Note_: All related content found in the `Age_Vs_Experience_Inference` Folder

### Tire Strategy vs. Driver Performance

_Note_: All related content found in the `Tire_strategy` Folder

### Home Advantage vs. Driver Performance

_Note_: All related content found in the `Home-field Advantage` Folder

### Gear Downshift Distance from Corners vs. Driver's Final Positions

_Note_: Navigate to `README` inside the `Gear_Downshift_Distance` folder for detailed instructions on how to view visualizations and run the code.

### Weather Conditions vs. Driver Performance

_Note_: All related content found in the `Weather Conditions` Folder

In the "data gathering script" folder, find the 'f1_weather_data_analysis.py' script for data collection. After running the script, it should produce five csv files used for data analysis. The "plots scripts" folder contains scripts to generate correlation and histogram plots either individually, or all together using "plots.py". Python 3.9.13 was used in making these scripts.
