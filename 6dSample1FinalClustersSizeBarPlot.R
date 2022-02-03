ggplot(Sample2MainClusterSizes, aes(x=Sample2MainClusters, y=Prct_posts, fill = as.factor(labels), reorder(labels))) + 
  geom_bar(stat="identity", position = 'dodge') + 
  labs(title='Sample 2 Main Clusters Size Distribution', x='Sample 2 Main Clusters', y='% of Total Posts in Cluster', fill='Clusters') + 
  geom_text(aes(label=prct), position = position_dodge(width = 0.9), vjust=-0.3, size=3.5) + 
  theme_minimal() + 
  theme(legend.position="none", text = element_text(), axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1, size = 13, face = 'bold')) + 
  scale_fill_manual(labels = c("Energy", "Carbon [emissions]", "Administration", "Climate Science", "Global Warming", "Population & Economy", "Plastic & Waste", "Agriculture", "Wildlife","Natural Catastrophes","General Posts","Unidentifiable"), values=c("#0048BA","#B0BF1A","black","#C46210","red","#3B7A57","pink","#FFBF00","#3DDC84","#C2B280","#00FFFF","#F400A1")) + 
  scale_y_continuous(limits=c(0,0.2), labels = scales::percent_format(accuracy = 1))