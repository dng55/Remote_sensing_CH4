col1 = FX2;
col2 = FY2(RT:-1:1,:);
% col3 = Lflux;

% combined = [col1;col2;col3]';

% csvwrite('FFP_csv_outputs/BB_fluxMap_x.csv',col1);
cd python_code/data

endFileName = 'june_aug2017.csv';

csvwrite(['BB_fluxMap_x_',endFileName],col1);

csvwrite(['BB_fluxMap_y_',endFileName],col2);

csvwrite(['BB_fluxMap_ch4_',endFileName],Lflux_ch4);

csvwrite(['BB_fluxMap_h_',endFileName],Lflux_h);

csvwrite(['BB_fluxMap_co2_',endFileName],Lflux_co2);