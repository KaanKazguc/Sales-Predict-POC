[English](README.md) | [Türkçe](README.tr.md) 

# AI Assistant POC That Calculates Sales Estimate for a Possible Market by Examining Surrounding Market Shopping Information

I have implemented the proof of concept of an artificial intelligence assistant that can estimate how much sales a potential store will make based on the sales information of stores in the same category in the vicinity. I worked with synthetic data on market sales to embody this concept, but it can be implemented for all types of stores that are located more than one in close proximity, such as restaurants and coffee shops. The people who can use the project prepared for use in a project are chain owners, wholesalers, and e-courier platform owners who have sales information of similar concept stores nearby.

Suppose we go a little more abstractly in the project. It is also possible to use it as an artificial intelligence that estimates the needs of nearby stores by looking at the products purchased through e-commerce.

![Logo](images/sales-estimate-logo.png)

## Related Projects

This project is designed to work integrated with the market control application.

[Market](https://github.com/HalilERT4S/Supermarket)

## Technologies Used

**API:** FastAPI

**Database:** SQL Server

**Python Libraries:** torch, pickle, pyodbc, pandas, numpy, dotenv, os

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`SERVER_NAME`

## Optimization

I wrote my own code that only calculates the co-occurrence rates to make the association analysis a bit faster. If you want to get more statistical data, you can use the industry standard `mlxtend` library.

## Feedback

If you have any feedback, please contact me at kaankazguc@hotmail.com.

## Thanks

- I would like to thank Professor Orhan ER, a faculty member at Bakircay University, Izmir, for taking the first step toward this project.

- I would like to thank [Omer Colakoglu](https://www.kaggle.com/omercolakoglu) for supporting me a lot with the datasets he published in synthetic data production.

- I would like to thank [@octokatherine](https://www.github.com/octokatherine) for making it easier for me to create the README file with the [Awesome README](https://github.com/matiassingers/awesome-readme) project.

- Also, my new closest friends ChatGPT, Gemini, and Claude for supporting me on this path ;)

## Attachments

Check out my Kaggle account to get the Market database with data in it. [Market Sales](https://www.kaggle.com/datasets/kaankc/market-satlar-ve-ilikisel-veri-taban)
