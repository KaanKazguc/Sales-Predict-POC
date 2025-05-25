
# Çevredeki Market Alışveriş Bilgilerini İnceleyerek Olası Bir Market İçin Satış Tahmini Hesaplayan AI Assistent POC 

Çevredeki aynı kategorideki mağzaların satış bilgilerinden yola çıkarak olası bir mağzanın ne kadar satış yapacağını tahmin edebilen bir yapay zeka asistan konseptinin kanıtını gerçekleştirdim. Bu konsepti somutlaştırmak için market satışları üzerinden sentetik veriler ile çalıştım ancak restoranlar, kahveciler gibi yakın mesafede birden fazla bulunan tüm dükkan türleri için gerçekleştirilebilir. Bir projede kullanmak için hazırlanan projeyi kullanabilecek kişiler yakın mesafedeki benzer konseptli dükkanların satış bilgilerini elinde tutan zincir sahipleri, toptancılar ve e-kurye platformu sahipleridir. 

Projede biraz daha soyutlamaya gidersek. E-ticaret ile alınan ürünlere bakarak çevredeki dükkan ihtiyaçlarını tahmin eden bir yapay zeka olarak da kullanmak mümkündür. 


![Logo](images/sales-estimate-logo.png)

    
## İlişkili Projeler

Bu proje market kontrol uygulaması ile entegre çalışacak şekilde tasarlanmıştır.

[Supermarket](https://github.com/matiassingers/awesome-readme)

  
## Kullanılan Teknolojiler

**API:** FastAPI

**Veri Tabanı:** SQL Server

**Python Kütüphaneleri:** torch, pickle, pyodbc, pandas, numpy, dotenv, os

  
## Ortam Değişkenleri

Bu projeyi çalıştırmak için aşağıdaki ortam değişkenlerini .env dosyanıza eklemeniz gerekecek

`SERVER_NAME`

  
## Optimizasyon

Birliktelik analizinin biraz daha hızlı hesaplanması için sadece birlikte görülme oranlarını hesaplayan kendi kodumu yazdım. Daha fazla istatistiksel veri elde etmek isterseniz sektör standartı olan `mlxtend` kütüphanesini kullanabilirsiniz.

  
## Geri Bildirim

Herhangi bir geri bildiriminiz varsa, lütfen kaankazguc@hotmail.com adresinden bana ulaşın.

  
## Teşekkürler

- Bu projeye adım atmama neden olduğu için İzmir Bakırçay Üniversitesi Öğretim Üyesi Profesör Orhan ER Hocama teşekkür ederim.

- Sentetik veri üretiminde yayınladığı veri setleri ile bana çok destek olan [Ömer ÇOLAKOĞLU](https://www.kaggle.com/omercolakoglu)'na teşekkür ederim.

- README dosyasını oluşturmamı [Awesome README](https://github.com/matiassingers/awesome-readme) projesi ile kolaylaştıran  [@octokatherine](https://www.github.com/octokatherine)'e teşekkür ederim.

- Ayrıca yeni en yakın arkadaşlarım ChatGPT, Gemini ve Claude bu yolda bana verdiğniz destekler için ;)

