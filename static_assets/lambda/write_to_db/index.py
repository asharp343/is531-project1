import json
import boto3
import os

def lambda_handler(event, context):
    
    rds = boto3.client('rds-data')
    
    create_table='''
    CREATE TABLE public.donuts (
      id int primary key,
      name character varying (500),
      link character varying (500),
      category character varying (500)
      )
               '''
    import_data = '''
            INSERT INTO public.donuts (id, name, link, category)
            VALUES (0, 'CINNAMON TOAST CRUNCH CINNAMON ROLL', 'https://www.krispykreme.com/getattachment/48dbe063-5539-42b2-a10e-0aa3c9d01fff/Cinnamon-Toast-Crunch-Cinnamon-Roll.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Glazed"]'),
            (1, 'ORIGINAL GLAZED CINNAMON ROLL', 'https://www.krispykreme.com/getattachment/3bd0c423-802b-4f5f-8b3f-c5ade48c25f7/Original-Glazed-Cinnamon-Roll.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Glazed"]'),
            (2, 'REESE’S CLASSIC DOUGHNUT', 'https://www.krispykreme.com/getattachment/2f349ff2-4997-456b-9e43-c3529251363c/REESE-S-Classic.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Filled"]'),
            (3, 'ORIGINAL FILLED
            ORIGINAL KREME™', 'https://www.krispykreme.com/getattachment/1a1f1807-a6d4-40af-9b51-5026065c8f6b/Original-Filled-Original-Kreme%E2%84%A2.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Iced", "Filled"]'),
            (4, 'ORIGINAL FILLED CHOCOLATE KREME™', 'https://www.krispykreme.com/getattachment/1818f984-fd98-44f9-b37c-c067adc63ce4/Original-Filled-Chocolate-Kreme%E2%84%A2.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Iced", "Chocolate", "Filled"]'),
            (5, 'ORIGINAL GLAZED®', 'https://www.krispykreme.com/getattachment/1aa956f7-e7ca-4e27-bcc6-a603211d7c68/Original-Glazed-Doughnut.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Glazed"]'),
            (6, 'CHOCOLATE ICED GLAZED', 'https://www.krispykreme.com/getattachment/0c798364-6391-471d-95eb-e0e5fb4e38e4/Chocolate-Iced-Glazed.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Iced", "Chocolate", "Glazed"]'),
            (7, 'CHOCOLATE ICED GLAZED WITH SPRINKLES', 'https://www.krispykreme.com/getattachment/07b4475d-4282-4729-a425-0bb24cd26f4d/Chocolate-Iced-Glazed-with-Sprinkles.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Iced", "Toppings", "Chocolate", "Glazed"]'),
            (8, 'OREO® COOKIES AND KREME', 'https://www.krispykreme.com/getattachment/43524412-f0a3-481b-b0d7-3eb7cc6288f4/OREO-Cookies-and-KREME.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Iced", "Toppings", "Filled", "OtherVarieties"]'),
            (9, 'CHOCOLATE ICED WITH KREME™ FILLING', 'https://www.krispykreme.com/getattachment/2da1a66a-78de-46c1-ab88-1715d69cf287/Chocolate-Iced-with-KREME-Filling.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Iced", "Chocolate", "Filled"]'),
            (10, 'CAKE BATTER', 'https://www.krispykreme.com/getattachment/7671b2a8-442c-4fbc-80ea-ef21d16c6673/Cake-Batter-Doughnut.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Iced", "Toppings", "Filled", "OtherVarieties"]'),
            (11, 'CHOCOLATE ICED CUSTARD FILLED', 'https://www.krispykreme.com/getattachment/2921a3c7-350a-4077-8194-5c8900a9a940/Chocolate-Iced-Custard-Filled.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Iced", "Chocolate", "Filled"]'),
            (12, 'GLAZED RASPBERRY FILLED', 'https://www.krispykreme.com/getattachment/2453215a-619a-40bd-a64b-1696f533d199/Glazed-Raspberry-Filled.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Filled", "Glazed", "Fruit"]'),
            (13, 'GLAZED LEMON FILLED', 'https://www.krispykreme.com/getattachment/0bd48216-d5a8-4838-885e-1e643a3a0e36/Glazed-Lemon-Filled.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Filled", "Glazed", "Fruit"]'),
            (14, 'STRAWBERRY ICED WITH SPRINKLES', 'https://www.krispykreme.com/getattachment/b138c5f6-13c2-4916-b028-f69432272444/Strawberry-Iced-with-Sprinkles.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Toppings", "Fruit"]'),
            (15, 'APPLE FRITTER', 'https://www.krispykreme.com/getattachment/e84619be-bce0-4239-8352-2117e1b66ad0/Apple-Fritter.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Glazed", "Fruit", "OtherVarieties"]'),
            (16, 'CHOCOLATE GLAZED DOUGHNUT', 'https://www.krispykreme.com/getattachment/9041db26-95ee-40e4-a069-1b6ca8d13b13/Chocolate-Glazed-Doughnut.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Chocolate", "Glazed"]'),
            (17, 'GLAZED WITH KREME™ FILLING', 'https://www.krispykreme.com/getattachment/2aa7568e-2b7e-4534-a70b-05f08162e879/Glazed-with-KREME-Filling.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Filled", "Glazed"]'),
            (18, 'CHOCOLATE ICED CAKE', 'https://www.krispykreme.com/getattachment/1d5b486e-45b0-4771-ab56-f44a2426baf7/Chocolate-Iced-Cake.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Iced", "Cake", "Chocolate"]'),
            (19, 'CHOCOLATE ICED RASPBERRY FILLED', 'https://www.krispykreme.com/getattachment/fee97a59-8427-4cbb-b5ee-cb387f578d85/Chocolate-Iced-Raspberry-Filled.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Iced", "Toppings", "Chocolate", "Filled", "Fruit", "OtherVarieties"]'),
            (20, 'GLAZED CHOCOLATE CAKE', 'https://www.krispykreme.com/getattachment/0cc91aab-7ead-4e5d-952a-88e909190a35/Glazed-Chocolate-Cake.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Cake", "Chocolate", "Glazed"]'),
            (21, 'GLAZED BLUEBERRY CAKE', 'https://www.krispykreme.com/getattachment/6b57c2f3-b56b-4b6c-8828-c63d0f99e32c/Glazed-Blueberry-Cake.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Cake", "Glazed", "Fruit"]'),
            (22, 'CINNAMON APPLE FILLED', 'https://www.krispykreme.com/getattachment/63312c7f-ff3a-4391-b35e-270852fa6717/Cinnamon-Apple-Filled.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Filled", "Fruit"]'),
            (23, 'CINNAMON BUN', 'https://www.krispykreme.com/getattachment/6869881c-ffe6-442e-b1a5-47ac503c1af6/Cinnamon-Bun.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Glazed", "OtherVarieties"]'),
            (24, 'CINNAMON SUGAR', 'https://www.krispykreme.com/getattachment/cbe20d75-913b-4ad7-9dc6-164d850395c4/Cinnamon-Sugar.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Toppings", "OtherVarieties"]'),
            (25, 'GLAZED SOUR CREAM', 'https://www.krispykreme.com/getattachment/84f85c76-bb0d-40b1-a9f4-0ca5ac8dd52c/Glazed-Sour-Cream.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Cake", "Glazed"]'),
            (26, 'TRADITIONAL CAKE', 'https://www.krispykreme.com/getattachment/d4841d35-ba1e-4708-9549-4dc52793ed39/Traditional-Cake.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Cake"]'),
            (27, 'CHOCOLATE ICED GLAZED CRULLER', 'https://www.krispykreme.com/getattachment/9e6fd86b-c813-46ef-be32-6526422998b5/Chocolate-Iced-Glazed-Cruller.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Iced", "Cake", "Chocolate", "Glazed"]'),
            (28, 'CINNAMON TWIST', 'https://www.krispykreme.com/getattachment/4fe0bd30-d7e6-4c1b-a7b5-218b9f88bc81/Cinnamon-Twist.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["OtherVarieties"]'),
            (29, 'DOUBLE DARK CHOCOLATE', 'https://www.krispykreme.com/getattachment/7137f4fe-f3b2-4b87-9d4f-55ed8cf6d85d/Double-Dark-Chocolate.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Iced", "Chocolate", "Filled", "OtherVarieties"]'),
            (30, 'DULCE DE LECHE', 'https://www.krispykreme.com/getattachment/90a71261-aecc-4206-b695-acab9926a443/Dulce-De-Leche.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Toppings", "Filled"]'),
            (31, 'GLAZED CINNAMON', 'https://www.krispykreme.com/getattachment/c8002aa7-853e-4097-ad35-1ab43b32cb24/Glazed-Cinnamon.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Toppings", "Glazed"]'),
            (32, 'GLAZED CRULLER', 'https://www.krispykreme.com/getattachment/d8f110d2-a357-473d-8c56-22dc80c9e073/Glazed-Cruller.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Cake", "Glazed"]'),
            (33, 'MAPLE ICED GLAZED', 'https://www.krispykreme.com/getattachment/dc92076b-0766-42c2-b6f4-63000e0f7af9/Maple-Iced-Glazed.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Iced", "Glazed"]'),
            (34, 'MINI ORIGINAL GLAZED® DOUGHNUTS', 'https://www.krispykreme.com/getattachment/a9bd1d66-c0c1-416a-8b6d-ac1bdb64486a/Mini-Original-Glazed-Doughnuts.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Glazed", "OtherVarieties"]'),
            (35, 'MINI CHOCOLATE ICED GLAZED', 'https://www.krispykreme.com/getattachment/5e920ad5-4b1e-4829-bd3f-1fd4c7a9050a/Mini-Chocolate-Iced-Glazed.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Iced", "Chocolate", "Glazed", "OtherVarieties"]'),
            (36, 'MINI CHOCOLATE ICED WITH SPRINKLES', 'https://www.krispykreme.com/getattachment/3c4db6b9-5997-41b1-8d51-4439d06f64e1/Mini-Chocolate-Iced-with-Sprinkles.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Iced", "Toppings", "Chocolate", "Glazed", "OtherVarieties"]'),
            (37, 'MINI STRAWBERRY ICED WITH SPRINKLES', 'https://www.krispykreme.com/getattachment/400bc5d6-98bd-4d2f-a157-48295f8a3b43/Mini-Strawberry-Iced-with-Sprinkles.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '[""]'),
            (38, 'NEW YORK CHEESECAKE', 'https://www.krispykreme.com/getattachment/fdcc4ab6-e90e-4c6d-88e2-7ca95d78f377/New-York-Cheesecake.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Iced", "Toppings", "Filled"]'),
            (39, 'POWDERED CAKE', 'https://www.krispykreme.com/getattachment/fb68570f-4549-45ae-a269-e45023b64695/Powdered-Cake.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Cake"]'),
            (40, 'POWDERED CINNAMON CAKE', 'https://www.krispykreme.com/getattachment/56792d34-6537-427d-abdb-401bba948a80/Powdered-Cinnamon-Cake.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Cake"]'),
            (41, 'POWDERED STRAWBERRY FILLED', 'https://www.krispykreme.com/getattachment/de7437d4-9d1a-40f3-b453-c5e511da0c4c/Powdered-Strawberry-Filled.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Toppings", "Filled", "Fruit"]'),
            (42, 'POWDERED WITH LEMON KREME', 'https://www.krispykreme.com/getattachment/5a180ed8-b70c-4f68-bb51-63ec4952da0c/Powdered-with-Lemon-Kreme.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Toppings", "Filled", "Fruit"]'),
            (43, 'POWDERED WITH STRAWBERRY KREME', 'https://www.krispykreme.com/getattachment/ab902bc0-3d50-4a7e-aca2-f90c07f68bd1/Powdered-with-Strawberry-Kreme.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Filled", "Fruit"]'),
            (44, 'STRAWBERRY ICED', 'https://www.krispykreme.com/getattachment/7ab68d1c-aa89-445a-9828-11bedd5817e2/Strawberry-Iced.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Iced", "Glazed", "Fruit"]'),
            (45, 'ORIGINAL GLAZED® DOUGHNUT HOLES', 'https://www.krispykreme.com/getattachment/edfafc3f-82bf-40f5-ae09-8896419c6f4a/Original-Glazed-Doughnut-Holes.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Glazed", "OtherVarieties"]'),
            (46, 'GLAZED CAKE DOUGHNUT HOLES', 'https://www.krispykreme.com/getattachment/8e641aa4-836f-4726-b5e6-2a11464af93e/Glazed-Cake-Doughnut-Holes.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Cake", "Glazed", "OtherVarieties"]'),
            (47, 'GLAZED BLUEBERRY CAKE DOUGHNUT HOLES', 'https://www.krispykreme.com/getattachment/73217a92-df7c-4703-a1d9-4e2c055ab454/Glazed-Blueberry-Cake-Doughnut-Holes.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Cake", "Glazed", "Fruit", "OtherVarieties"]'),
            (48, 'GLAZED CHOCOLATE CAKE DOUGHNUT HOLES', 'https://www.krispykreme.com/getattachment/c9dca2e7-fcb6-4c03-b41b-89d0075b66b6/Glazed-Chocolate-Cake-Doughnut-Holes.aspx?width=310&height=310&mode=max&quality=60&format=jpg', '["Cake", "Chocolate", "Glazed", "OtherVarieties"]');'''

    response_create_table = rds.execute_statement(
        resourceArn = os.environ['CLUSTER_ARN'],
        secretArn = os.environ['SECRET_ARN'],
        sql = create_table
    )
    
    response_import_data = rds.execute_statement(
        resourceArn = os.environ['CLUSTER_ARN'],
        secretArn = os.environ['SECRET_ARN'],
        sql = import_data
    )
    
    
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('done')
    }