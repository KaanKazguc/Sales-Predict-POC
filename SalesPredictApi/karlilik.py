import torch
import torch.nn as nn
import numpy as np

class MarketSalesModel(nn.Module):
    def __init__(self, input_dims):
        super(MarketSalesModel, self).__init__()

        self.main_market_net = nn.Sequential(
            nn.Linear(input_dims['main_market'], 16),
            nn.ReLU(),
            nn.BatchNorm1d(16),
            nn.Dropout(0.2),
            nn.Linear(16, 8),
            nn.ReLU()
        )

        self.item_net = nn.Sequential(
            nn.Linear(input_dims['item'], 32),
            nn.ReLU(),
            nn.BatchNorm1d(32),
            nn.Dropout(0.2),
            nn.Linear(32, 16),
            nn.ReLU()
        )

        self.near_market1_net = nn.Sequential(
            nn.Linear(input_dims['near_market1'], 32),
            nn.ReLU(),
            nn.BatchNorm1d(32),
            nn.Dropout(0.2),
            nn.Linear(32, 16),
            nn.ReLU()
        )

        self.near_market2_net = nn.Sequential(
            nn.Linear(input_dims['near_market2'], 32),
            nn.ReLU(),
            nn.BatchNorm1d(32),
            nn.Dropout(0.2),
            nn.Linear(32, 16),
            nn.ReLU()
        )

        self.near_market3_net = nn.Sequential(
            nn.Linear(input_dims['near_market3'], 32),
            nn.ReLU(),
            nn.BatchNorm1d(32),
            nn.Dropout(0.2),
            nn.Linear(32, 16),
            nn.ReLU()
        )

        combined_size = 8 + 16 + 16 + 16 + 16
        self.combined_net = nn.Sequential(
            nn.Linear(combined_size, 64),
            nn.ReLU(),
            nn.BatchNorm1d(64),
            nn.Dropout(0.3),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(32, 1)
        )

    def forward(self, x_dict):
        main_market_out = self.main_market_net(x_dict['main_market'])
        item_out = self.item_net(x_dict['item'])
        near_market1_out = self.near_market1_net(x_dict['near_market1'])
        near_market2_out = self.near_market2_net(x_dict['near_market2'])
        near_market3_out = self.near_market3_net(x_dict['near_market3'])

        combined = torch.cat([
            main_market_out,
            item_out,
            near_market1_out,
            near_market2_out,
            near_market3_out
        ], dim=1)

        output = self.combined_net(combined)
        return output


def predict_sales(model, market_data, scalers, label_encoders, device):
    model.eval()
    processed_data = market_data.copy()

    for col in ['ITEMCODE', 'CAT']:
        if col in processed_data.columns:
            le = label_encoders[col]
            processed_data[col] = le.transform(processed_data[col])

    main_market_features = processed_data[['Alan']].values
    item_features = processed_data[['ITEMCODE', 'CAT']].values
    near_market1_features = processed_data[['Alan1', 'Distance_m1', 'ToplamSatis1']].values
    near_market2_features = processed_data[['Alan2', 'Distance_m2', 'ToplamSatis2']].values
    near_market3_features = processed_data[['Alan3', 'Distance_m3', 'ToplamSatis3']].values

    scaled_features = {
        'main_market': scalers['main_market'].transform(main_market_features),
        'item': scalers['item'].transform(item_features),
        'near_market1': scalers['near_market1'].transform(near_market1_features),
        'near_market2': scalers['near_market2'].transform(near_market2_features),
        'near_market3': scalers['near_market3'].transform(near_market3_features)
    }

    tensor_features = {k: torch.FloatTensor(v).to(device) for k, v in scaled_features.items()}

    with torch.no_grad():
        predictions = model(tensor_features)

    return predictions.cpu().numpy()
