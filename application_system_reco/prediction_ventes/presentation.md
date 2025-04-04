Soit **prediction_list** un dictionnaire associant à chaque livre **k** un score $kv$.  
On définit **max_score** comme le score maximal parmi tous les livres.  
On transforme chaque score selon la formule :  
$$\
p_k = \max\left(0.1, \min\left(1, \frac{v_k}{\max\_score} \right) \right)
$$

où :  
- $v_k$ est le poids initial du livre \( k \),  
- $\max\_score = \max(v_k)$ est le score maximal dans la liste,  
- $p_k$ est le score normalisé du livre \( k \), borné entre 0.1 et 1.  