ggplot(Sample2_UMAP_12MainClusters, aes(UMAPx, UMAPy, colour = as.factor(labels))) + 
  geom_point() + 
  scale_color_manual(labels = c("Energy", "Carbon [emissions]", "Administration", "Climate Science", "Global Warming", "Population & Economy", "Plastic & Waste", "Agriculture", "Wildlife","Natural Catastrophes","General Posts","Unidentifiable"), values=c("#0048BA", "#B0BF1A", "black", "#C46210","red","#3B7A57","pink","#FFBF00","#3DDC84","#C2B280","#00FFFF","#F400A1")) + 
  labs(title='Sample 2 Main Clusters Scatter Plot', color='Clusters') + 
  guides(colour = guide_legend(override.aes = list(size=6)))
