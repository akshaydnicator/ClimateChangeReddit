# This script was used to visualize the distribution of size of the final optimized clusters for Sample 1 using Bar plot

# Load required libraries
library(ggplot2)

# Read data
Sample1MainClusterSizes <- read.csv("C:/Users/Akshay Kaushal/Desktop/Desktop/Akki/Data Analytics/ClimateChange/Kaggle/Sample1FinalClusterSizes.csv")

# Create a factor of the main clusters columns
Sample1MainClusterSizes$Sample1MainClusters <- factor(Sample1MainClusterSizes$Sample1MainClusters, levels = Sample1MainClusterSizes$Sample1MainClusters)

# Create the bar plot for final optimized clusters
ggplot(Sample1MainClusterSizes, aes(x=Sample1MainClusters, y=Prct_posts, fill = as.factor(labels), reorder(labels))) +
  geom_bar(stat="identity", position = 'dodge') + 
  labs(title='Sample 1 - Optimized clusters size distribution', x='Sample 1 Optimized clusters', y='% of total posts in cluster', fill='Clusters') + 
  geom_text(aes(label=prct), position = position_dodge(width = 0.9), vjust=-0.3, size=6) + 
  theme_minimal() + 
  theme(legend.position="none", axis.text = element_text(size=18), axis.title = element_text(size = 20), plot.title = element_text(size = 22, hjust = 0.5),  axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1, colour = "black", size = 20), axis.text.y = element_text()) +  
  scale_fill_manual(labels = c("Energy", "Carbon [emissions]", "Administration", "Climate Science", "Global Warming", "Population & Economy", "Plastic & Waste", "Agriculture & Administration", "Wildlife","Natural Catastrophes","General Posts","Unidentifiable"), values=c("#0048BA","#B0BF1A","black","#C46210","red","#3B7A57","pink","#FFBF00","#3DDC84","#C2B280","#00FFFF","#F400A1")) + 
  scale_y_continuous(limits=c(0,0.2), labels = scales::percent_format(accuracy = 1))
