from lxml import html
import requests

games = {
    'WOLF NEW ORDER         :::https://ebgames.com.au/xbox-one-165287-wolfenstein-the-new-order-preowned-xbox-one',
    'WOLF OLD BLOOD         :::https://ebgames.com.au/xbox-one-208413-wolfenstein-the-old-blood-preowned-xbox-one',
    'FALLOUT 4              :::https://ebgames.com.au/xbox-one-202582-fallout-4-preowned-xbox-one',
    'DEUS EX                :::https://ebgames.com.au/xbox-one-208246-deus-ex-mankind-divided-preowned-xbox-one',
    'DESTINY                :::https://ebgames.com.au/xbox-one-165247-destiny-preowned-xbox-one',
    'DOOM                   :::https://www.ebgames.com.au/xbox-one-201660-DOOM-preowned-Xbox-One',
    'BATMAN ARKHAM KNIGHT   :::https://ebgames.com.au/xbox-one-200007-Batman-Arkham-Knight-preowned-Xbox-One',
    'RECORE                 :::https://ebgames.com.au/xbox-one-206798-ReCore-preowned-Xbox-One',
    'HALO 5: GUARDIANS      :::https://ebgames.com.au/xbox-one-165256-Halo-5-Guardians-preowned-Xbox-One',
    'METAL GEAR SOLID V GZ  :::https://ebgames.com.au/xbox-one-165265-Metal-Gear-Solid-V-Ground-Zeroes-preowned-Xbox-One',
    'Dishonored 2 LE        :::https://ebgames.com.au/xbox-one-202587-Dishonored-2---Limited-Edition-Xbox-One',
    'MORTAL COMBAT Xbox     :::https://ebgames.com.au/xbox-one-202483-Mortal-Kombat-X-Xbox-One',
    'Metal Gear Solid V TPP :::https://ebgames.com.au/xbox-one-165266-Metal-Gear-Solid-V-The-Phantom-Pain-preowned-Xbox-One',
    'The Witcher 3 Wild Hunt:::https://ebgames.com.au/xbox-one-165282-The-Witcher-3-Wild-Hunt-preowned-Xbox-One',
    'TITANFALL 2            :::https://ebgames.com.au/xbox-one-216077-Titanfall-2-preowned-Xbox-One',
    'FOR HONOR              :::https://ebgames.com.au/xbox-one-206806-For-Honor-preowned-Xbox-One',
    'RISE OF THE TOMB RAIDER:::https://ebgames.com.au/xbox-one-202510-Rise-of-the-Tomb-Raider-preowned-Xbox-One',
    'BIOSHOCK COLLECTION    :::https://ebgames.com.au/xbox-one-221607-Bioshock-The-Collection-preowned-Xbox-One',
    'GEARS OF WAR 4         :::https://ebgames.com.au/xbox-one-206794-Gears-of-War-4-preowned-Xbox-One',
    'FORZA HORIZON 3        :::https://ebgames.com.au/xbox-one-220705-Forza-Horizon-3-preowned-Xbox-One',
    'HITMAN COMPLETE SEASON :::https://ebgames.com.au/xbox-one-165257-HITMAN-The-Complete-First-Season-preowned-Xbox-One',
    'INJUSTICE 2            :::https://ebgames.com.au/xbox-one-217280-Injustice-2-Xbox-One',
}

xpath = '//*[@id="content"]/div/div[1]/div[2]/div[1]/div[2]/div[2]/div/div/div[1]/div[2]/text()'
for gameData in games:
    gameTitle = gameData.split(':::')[0]
    gameURL = gameData.split(':::')[1]
    page = requests.get(gameURL)
    tree = html.fromstring(page.content)
    price = tree.xpath(xpath)
    print (gameTitle, ':', price)