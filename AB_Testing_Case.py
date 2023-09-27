#####################################################
# AB Testi ile Bidding Yöntemlerinin Dönüşümünün Karşılaştırılması
#####################################################


######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################

# 1. Hipotezleri Kur
# 2. Varsayım Kontrolü
#   - 1. Normallik Varsayımı (shapiro)
#   - 2. Varyans Homojenliği (levene)
# 3. Hipotezin Uygulanması
#   - 1. Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi
#   - 2. Varsayımlar sağlanmıyorsa mannwhitneyu testi
# 4. p-value değerine göre sonuçları yorumla
# Not:
# - Normallik sağlanmıyorsa direkt 2 numara. Varyans homojenliği sağlanmıyorsa 1 numaraya arguman girilir.
# - Normallik incelemesi öncesi aykırı değer incelemesi ve düzeltmesi yapmak faydalı olabilir.

import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# !pip install statsmodels           
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)


#####################################################
# Görev 1:  Veriyi Hazırlama ve Analiz Etme
#####################################################

# Adım 1:  ab_testing_data.xlsx adlı kontrol ve test grubu verilerinden oluşan veri setini okutunuz.
#          Kontrol ve test grubu verilerini ayrı değişkenlere atayınız.

control_group = pd.read_excel("Measurement_Problems/Case2 - AB Testing/ab_testing.xlsx", sheet_name='Control Group')
test_group = pd.read_excel("Measurement_Problems/Case2 - AB Testing/ab_testing.xlsx", sheet_name='Test Group')


# Adım 2: Kontrol ve test grubu verilerini analiz ediniz.

control_group.head()
control_group.shape               # (40, 4)
control_group.info()
control_group.describe().T
control_group.isnull().sum()      # 0

test_group.head()
test_group.shape                # (40, 4)
test_group.info()               # float64
test_group.describe().T         # purchase mean daha yüksek.
test_group.isnull().sum()       # 0

# Adım 3: Analiz işleminden sonra concat metodunu kullanarak kontrol ve test grubu verilerini birleştiriniz.

A = pd.DataFrame(control_group["Purchase"])
B = pd.DataFrame(test_group["Purchase"])

AB = pd.concat([A,B],axis=1)
AB.columns=["A","B"]
AB.head()


#####################################################
# Görev 2:  A/B Testinin Hipotezinin Tanımlanması
#####################################################

# Adım 1: Hipotezi tanımlayınız.
# H0 : M1 = M2       İki teklif türünün kazanç ortalamaları arasında farkı yoktur.
# H1 : M1!= M2

# Adım 2: Kontrol ve test grubu için purchase(kazanç) ortalamalarını analiz ediniz
control_group["Purchase"].mean()     # 550.894
test_group["Purchase"].mean()        # 582.106
# Fark var gibi fakat şans eseri mi?


#####################################################
# GÖREV 3: Hipotez Testinin Gerçekleştirilmesi
#####################################################

# Adım 1: Hipotez testi yapılmadan önce varsayım kontrollerini yapınız.Bunlar Normallik Varsayımı ve Varyans Homojenliğidir.
#         Kontrol ve test grubunun normallik varsayımına uyup uymadığını Purchase değişkeni
#         üzerinden ayrı ayrı test ediniz.


# Normallik varsayımı

test_stat, pvalue = shapiro(A.dropna())
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# p-value = 0.5891

test_stat, pvalue = shapiro(B.dropna())
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# p-value = 0.1541

# Normallik varsayımı reddedilemedi. p değerleri 0.05'ten büyük.


# Varyans homojenliği

test_stat, pvalue = levene(AB.A,AB.B)
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# p-value = 0.1083  olduğu için H0 reddedilemedi.



# Adım 2: Normallik Varsayımı ve Varyans Homojenliği sonuçlarına göre uygun testi seçiniz.

# Varsayımlar sağlandığı için bağımsız iki örneklem T Testi uygulanır.



# Adım 3: Test sonucunda elde edilen p_value değerini göz önünde bulundurarak kontrol ve test grubu satın alma
# ortalamaları arasında istatistiki olarak anlamlı bir fark olup olmadığını yorumlayınız.

test_stat, pvalue = ttest_ind(AB.A,AB.B,equal_var=True)
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# p-value = 0.3493  değeri 0.05'ten büyük olduğu için H0 reddedilemez. İki teklif arasında istatistiksel olarak anlamlı bir fark yoktur.



##############################################################
# GÖREV 4 : Sonuçların Analizi
##############################################################

# Adım 1: Hangi testi kullandınız, sebeplerini belirtiniz.

# İki grubun ortalamaları arasında fark olup olmadığını istatistiksel açıdan kanıtlamak istedik.
# Normallik varsayımı ve varyans homojenliği sonuçlarında hipotez reddedilemedi. Varsayımlar sağlandığı için bağımsız iki örneklem T testi kullandık.
# Bunun sonucunda elde edilen p değeri 0.05'ten büyük olduğu için hipotezimiz istatistiksel olarak %95 güvenle doğrulandı.
# Yani iki grubun ortalamaları arasında anlamlı bir fark yoktur.


# Adım 2: Elde ettiğiniz test sonuçlarına göre müşteriye tavsiyede bulununuz.

# İki yöntemden biri seçilebilir. Diğer etkileşim koşulları göz önünde bulundurulabilir.
# Test süresi arttırılabilir.
