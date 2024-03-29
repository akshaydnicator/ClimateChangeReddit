# This script was used to visualize the 2D UMAP components obtained from previous step for Sample 2 with a scatter plot

# Load required libraries
library(ggplot2)

# Read data
UMAPSample2 <- read.csv("C:/Users/Akshay Kaushal/Desktop/Desktop/Akki/Data Analytics/ClimateChange/UMAPComponentsSample2.csv", row.names=1)

# Create the scatter plot for final optimized clusters
ggplot(UMAPSample2, aes(UMAPx, UMAPy, colour = as.factor(labels))) + 
  geom_point() + 
  scale_color_manual(labels = c("Energy", "Carbon [emissions]", "Administration", "Climate science", "Global warming", "Population & economy", "Plastic & waste", "Agriculture", "Wildlife","Natural catastrophes","General posts","Unidentifiable"), values=c("#0048BA", "#B0BF1A", "black", "#C46210","red","#3B7A57","pink","#FFBF00","#3DDC84","#C2B280","#00FFFF","#F400A1")) + 
  labs(title='Sample 2 - Optimized clusters scatter plot', color='Sample 2: Optimized clusters') +
  guides(colour = guide_legend(override.aes = list(size=10))) +
  theme(axis.text = element_text(size=18), axis.title = element_text(size = 20), plot.title = element_text(size = 22, hjust = 0.5), legend.text = element_text(size = 20), legend.title = element_text(size = 20)) +
  scale_y_continuous(labels = scales::number_format(accuracy = 1))
