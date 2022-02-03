# This script was used to visualize the 2D UMAP components obtained from previous step with a scatter plot

# Load required libraries
library(ggplot2)

# Read data
UMAPSample1 <- read.csv("C:/Users/Akshay Kaushal/Desktop/Desktop/Akki/Data Analytics/ClimateChange/UMAPComponentsSample1.csv", row.names=1)

# Create the scatter plot for final optimized clusters
ggplot(UMAPSample1, aes(UMAPx, UMAPy, colour = as.factor(labels))) +
  geom_point() +
  scale_color_manual(labels = c("Energy", "Carbon [emissions]", "Administration", "Climate Science", "Global Warming", "Population & Economy", "Plastic & Waste", "Agriculture & Administration", "Wildlife","Natural Catastrophes","General Posts","Unidentifiable"), values=c("#0048BA", "#B0BF1A", "black", "#C46210","red","#3B7A57","pink","#FFBF00","#3DDC84","#C2B280","#00FFFF","#F400A1")) +
  labs(title='Sample 1 Main Clusters Scatter Plot', color='Clusters') +
  guides(colour = guide_legend(override.aes = list(size=6)))