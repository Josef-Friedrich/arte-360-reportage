#! /usr/bin/env python


import json
import glob
import re
import difflib
import typing
import pathlib

files = """
_new/Ahornsirup - Kanadas süßer Schatz (ARTE 360° Reportage) [HlFRnPw6Y04].mp4
_new/Åland-Archipel, warten auf das Eis (360° - GEO Reportage) [cZG6qlbVXCY].mp4
_new/Alligatorjagd in Florida (360° - GEO Reportage) [Ky2m06TY8NY].mp4
_new/Alphadi und die Farben der Wüste (360° - GEO Reportage) [y9UDkxFqr0s].mp4
_new/Amas Welt, das neue Ghana (360° - GEO Reportage) [xLgEiCxyZ3k].mp4
_new/An den Ufern der Loire (360° - GEO Reportage) [u-rV3o70aFs].mp4
_new/Anatolien, das Land wo die Aprikosen blühen (360° - GEO Reportage) [6UNZBLK5xHc].mp4
_new/Andalusien - Edle Pferde, wilde Stiere (360° - GEO Reportage) [9ZTsCCSztp0].mp4
_new/Arganöl - Marokkos weißes Gold (360° - GEO Reportage) [hebFHCqfu0c].mp4
_new/Argentinien, von wilden Pferden und sanfter Hand (360° - GEO Reportage) [UTT1hwyKwrw].mp4
_new/Arktis - Die Route der Atomeisbrecher (360° - GEO Reportage) [4VEpfXzy214].mp4
_new/Arktis - ein Junge wird Jäger (360° - GEO Reportage) [9ff-GcgySN4].mp4
_new/Armenien, die Früchte aus dem Paradies (360° - GEO Reportage) [25Vub7M_rLc].mp4
_new/Atacamawüste - Leben ohne Wasser (360° - GEO Reportage) [OJJze1tQhz0].mp4
_new/Attila und die Pferde der Puszta (360° - GEO Reportage) [Cbc64mnqRck].mp4
_new/Aubrac - Kühe, Käse, Kerle! (360° - GEO Reportage) [FKXxagKURQM].mp4
_new/Auf dem Floß durch die Schluchten der Tara (360° - GEO Reportage) [H9eSAANUh54].mp4
_new/Auf den Dächern von Kairo (360° - GEO Reportage) [6rS22dz6_7o].mp4
_new/Auf den Spuren der Wikinger (360° - GEO Reportage) [Zsj8iSV3nQE].mp4
_new/Auf der Spur des spanischen Luchses (360° - GEO Reportage) [ou7f1H60z7Q].mp4
_new/Auf Schlangenfang in Kambodscha (360° - GEO Reportage) [qVuhqpYiH5c].mp4
_new/Australien - Wenn Kunst auf Silos trifft (360° - GEO Reportage) [G8JDOqwLGog].mp4
_new/Azoren, das Geschäft mit den Walen (360° - GEO Reportage) [GUO0RvRiuQE].mp4
_new/Bahamas - unverfälscht! (360° - GEO Reportage) [GGxlN3DjKCI].mp4
_new/Baikalsee - ein Wintermärchen (360° - GEO Reportage) [Q32TkfdHpnI].mp4
_new/Bangkoks krabbelnde Delikatessen (360° - GEO Reportage) [Cxe2KMNhjG0].mp4
_new/Bangkoks Schatztaucher (360° - GEO Reportage) [RKq3lqts3lg].mp4
_new/Bangladesh, Schiff der Hoffnung (360° - GEO Reportage) [4H01x3_OEaY].mp4
_new/Basketball - Die kleinen Barfußspieler von Mexiko (360° - GEO Reportage) [AskLUCcfDuI].mp4
_new/Bhutan, von Kindern und Kranichen (360° - GEO Reportage) [jlJuiIMhBqQ].mp4
_new/Biber, die Baumeister an der Elbe (360° - GEO Reportage) [X8fy7jZl_rE].mp4
_new/Biberkrieg in Bayern (360° - GEO Reportage) [L1QY4QuRJs4].mp4
_new/Bird Island - Allein unter Pinguinen (360° - GEO Reportage) [Wlc3mjQr5ek].mp4
_new/Bishnoi, Tierliebe bis in den Tod (360° - GEO Reportage) [tcNmq-quVPA].mp4
_new/Bisons, die sanften Riesen von Montana (360° - GEO Reportage) [HwOJJFzY5Cc].mp4
_new/Bolivien - Der Kampf um die kleinen Herzen (360° - GEO Reportage) [Brrl86VTvq4].mp4
_new/Bolivien - Kleine Käfer, großes Geld! (360° - GEO Reportage) [jOGkfs9xLlk].mp4
_new/Bolivien, Lebensader Todesstraße (360° - GEO Reportage) [JhplvCSCDkQ].mp4
_new/Boliviens junge Wilde (360° - GEO Reportage) [SfnqxRXIJSo].mp4
_new/Brasilien - Büffel auf Streife (360° - GEO Reportage) [J3OzpZ5L3o8].mp4
_new/Bretagne, die raue Schönheit (360° - GEO Reportage) [o6cVARiIZGA].mp4
_new/Bretagne, von Bienen und Leuchttürmen (360° - GEO Reportage) [FskHAYwU3FM].mp4
_new/Buddhas Kinder im Goldenen Dreieck (360° - GEO Reportage) [5_SK0AFJqfQ].mp4
_new/Carmargue, zwischen Himmel und Meer (360° - GEO Reportage) [8bnLFaEqSeA].mp4
_new/Champagner für alle! (360° - GEO Reportage) [cV-MNXIukmA].mp4
_new/Chartres, die Farben des Himmels (360° - GEO Reportage) [qPLtZngzS10].mp4
_new/Chile - Segen und Fluch einer Kupfermine (360° - GEO Reportage) [SvRfFmEL43Y].mp4
_new/Chile, die Leuchttürme am Ende der Welt (360° - GEO Reportage) [u1jaUHMhRwo].mp4
_new/China - Die Eisfischer vom Chagan-See (360° - GEO Reportage) [vPLT2RVso_Y].mp4
_new/China, Braut ohne Bräutigam (360° - GEO Reportage) [e9nzSo2Tqr8].mp4
_new/China, im Reich der Musuo-Frauen (360° - GEO Reportage) [GhMq7fkeUKI].mp4
_new/Chivas - Kolumbiens bunte Busse (360° - GEO Reportage) [-Min0yF6ccg].mp4
_new/Churubamba - Frauen am Ball (360° - GEO Reportage) [4S_yDEomrcY].mp4
_new/Cocos Island - Insel der Haie (360° - GEO Reportage) [A-aSNeoHaGI].mp4
_new/Cook Islands - Welcome to Paradise! (360° - GEO Reportage) [0Hn3y3DIcl4].mp4
_new/Costa Rica - Leben wie die Faultiere (360° - GEO Reportage) [NpxUVkA3Dfs].mp4
_new/Costa Rica, das größte Hundeheim der Welt (360° - GEO Reportage) [5N1mFKBBFLg].mp4
_new/Cranberrysaison auf Cape Cod (360° - GEO Reportage) [YZ7wxrTF3uI].mp4
_new/Curaçao - Die sanften Delfine (360° - GEO Reportage) [wc4y3QIarAU].mp4
_new/Dagestan – Land über den Wolken (360° - GEO Reportage) [E0QU7u1xbFM].mp4
_new/Dänemark - Königin Margrethe und ihr Sommerschloss (360° - GEO Reportage) [qIrnygvh_I8].mp4
_new/Das Dschungel-Orchester (360° - GEO Reportage) [Q1sjNpil_Fw].mp4
_new/Das Elefantenkrankenhaus von Thailand (360° - GEO Reportage) [stCFbtfBtcI].mp4
_new/Das Elsass - Land der Orgeln (360° - GEO Reportage) [Ef81fAqnuJs].mp4
_new/Das Elsass, Heimat der Störche (360° - GEO Reportage) [BZaILC2jnoM].mp4
_new/Das Geheimnis der Schweizer Uhren (360° - GEO Reportage) [WhhdUVCFga0].mp4
_new/Das Kinderparlament von Rajasthan (360° - GEO Reportage) [1I5rUoMUmwA].mp4
_new/Das Koala-Hospital (360° - GEO Reportage) [f4ODAYWj-MA].mp4
_new/Das Mysterium der sibirischen Mumie (360° - GEO Reportage) [DXk26Rs6ev8].mp4
_new/Das Perlenimperium von Palawan (360° - GEO Reportage) [7KKgclOqxAU].mp4
_new/Das Postschiff zum Ende der Welt (360° - GEO Reportage) [hnuma6p1K08].mp4
_new/Das Salz der Inka (360° - GEO Reportage) [RUfLIGurIAE].mp4
_new/Das schwimmende Krankenhaus vom Amazonas (360° - GEO Reportage) [0Xz-nWoBhUQ].mp4
_new/Das Terrassenwunder von Peru (360° - GEO Reportage) [0-cZ-g6esRw].mp4
_new/Das Vermächtnis der Marquesas-Inseln (360° - GEO Reportage) [7FS3M6gwn2g].mp4
_new/Das Whisky-Geheimnis von Islay (360° - GEO Reportage) [4z_vcFuiwds].mp4
_new/David und die Komodowarane (360° - GEO Reportage) [6uFzOGhS8UI].mp4
_new/Dem Wolf auf der Spur - Schnüffeln für den Artenschutz (360° - GEO Reportage) [8zqR15KTGN4].mp4
_new/Der Affenflüsterer und sein Traum (360° - GEO Reportage) [tsXjqdQkSio].mp4
_new/Der Andenkondor, König der Lüfte (360° - GEO Reportage) [c0y6PT21TCs].mp4
_new/Der Exzentriker der Düfte (360° - GEO Reportage) [qP99-RnEm7U].mp4
_new/Der fröhliche Friedhof von Rumänien (360° - GEO Reportage) [kYW3GLZS5tA].mp4
_new/Der gute Mensch von Karachi (360° - GEO Reportage) [pk9M0hHj6e4].mp4
_new/Der Kosakenpriester vom Don (360° - GEO Reportage) [RdAzR4VEOHA].mp4
_new/Der Kräutergarten von Java (360° - GEO Reportage) [n_GzJ5oxdSQ].mp4
_new/Der Lachszähler von Kamtschatka (360° - GEO Reportage) [_1z6gndFCQg].mp4
_new/Der Lachszähler von Kanada (360° - GEO Reportage) [QM_8fpHN6Jo].mp4
_new/Der letzte Rheinfischer (360° - GEO Reportage) [1JPQTQtsjyA].mp4
_new/Der Maestro, Neapels legendärer Boxmeister (360° - GEO Reportage) [KVIq8lwVpD4].mp4
_new/Der Otter-Mann von Ungarn (360° - GEO Reportage) [7TUDH-k4qH0].mp4
_new/Der Polarflieger (360° - GEO Reportage) [JudMONhb6p0].mp4
_new/Der Thomanerchor - Leben für die Musik (360° - GEO Reportage) [931l1cfsbDg].mp4
_new/Der Traum vom Gold - Tirols Überfliegerinnen (360° - GEO Reportage) [9z8Eer2KngU].mp4
_new/Der Waldrapp - Punkvogel aus den Alpen (360° - GEO Reportage) [WDNIqAtjJnE].mp4
_new/Der Weinpriester von Bali (360° - GEO Reportage) [-D0iE7FsRGQ].mp4
_new/Der weiße Berg von Feuerland (360° - GEO Reportage) [N1vjuQX9RyY].mp4
_new/Der Wüstendoktor (360° - GEO Reportage) [FxPvLeQmgok].mp4
_new/Der Wüstenzug, die Lebensader Mauretaniens (360° - GEO Reportage) [k9jFka2IecU].mp4
_new/Dhaus, Arabiens legendäre Schiffe (360° - GEO Reportage) [07X5I9kJvS4].mp4
_new/Die Austern von Arcachon (360° - GEO Reportage) [JCjShQJ89x0].mp4
_new/Die Bärenhunde von Nevada (360° - GEO Reportage) [wf024fhwmvw].mp4
_new/Die Baumkletterer von Kalifornien (360° - GEO Reportage) [CP6G2KgHMR4].mp4
_new/Die Bergführer vom Mont Blanc (360° - GEO Reportage) [l7mRLjiZ1Tw].mp4
_new/Die Bergführer von San Martino (360° - GEO Reportage) [rqDUm-WpZJ0].mp4
_new/Die blinde Primaballerina von Sao Paulo (360° - GEO Reportage) [NXWsLpDP-Mc].mp4
_new/Die Bogenschützin von Bhutan (360° - GEO Reportage) [wyIXpjaP9VM].mp4
_new/Die einsamen Mönche von Oelenberg (360° - GEO Reportage) [QR5RWf0_ksc].mp4
_new/Die Eisbergjäger von Neufundland (360° - GEO Reportage) [Jylj5OMHrWk].mp4
_new/Die Eisenbahn vom Baikal zum Amur (360° - GEO Reportage) [GTkxMy9yVZM].mp4
_new/Die Falkenärztin von Abu Dhabi (360° - GEO Reportage) [QE2i1lYmb_Q].mp4
_new/Die Feuerflieger von Valencia (360° - GEO Reportage) [hc_-HyJy6u0].mp4
_new/Die Feuerspringer von Sibirien (360° - GEO Reportage) [fh2Pl9u1XOw].mp4
_new/Die Geier sind zurück (360° - GEO Reportage) [e5A0glDrlkU].mp4
_new/Die goldenen Schildkröten von Madagaskar (360° - GEO Reportage) [Do-ZlyolY9I].mp4
_new/Die Halligen mitten im Winter, mitten im Wasser (360° - GEO Reportage) [qZMtcyipMQc].mp4
_new/Die Herren des Lavendels (360° - GEO Reportage) [KEOwqcBWE2s].mp4
_new/Die Holzfäller von British Columbia (360° - GEO Reportage) [MpF684mvA5A].mp4
_new/Die Honigsammler von Yunnan (360° - GEO Reportage) [ddARBEV3fH4].mp4
_new/Die Igel-Retter aus dem Piemont (360° - GEO Reportage) [FN8ybVCWbVw].mp4
_new/Die Kämpferinnen von Mexiko (360° - GEO Reportage) [HDZDyBBnqDs].mp4
_new/Die Kichwa-Krieger und das Öl (360° - GEO Reportage) [t3Kiy1Iz69k].mp4
_new/Die kleinen Schätze in Frankreichs Gärten (360° - GEO Reportage) [6eWUfGWASTA].mp4
_new/Die Köchin von Bahia (360° - GEO Reportage) [U0f-lOEyArs].mp4
_new/Die Krabbenfischer von Feuerland (360° - GEO Reportage) [Y8D9o5YD2dM].mp4
_new/Die Krabbenflut (360° - GEO Reportage) [Unop9XcUC7g].mp4
_new/Die letzten Cowboys der Toskana (360° - GEO Reportage) [We74sUq6TL8].mp4
_new/Die letzten Kamelkarawanen der Sahara (360° - GEO Reportage) [kKr2LCU__Pg].mp4
_new/Die letzten Köhler von Rumänien (360° - GEO Reportage) [NaYD2IlnDXw].mp4
_new/Die letzten Krokodile Venezuelas (360° - GEO Reportage) [p9sjFVILLlo].mp4
_new/Die letzten Walfänger der Beringsee (360° - GEO Reportage) [IlG92mvmCEI].mp4
_new/Die Liebenden von Santa Cruz del Islote (360° - GEO Reportage) [UNPolG8VXFo].mp4
_new/Die Lowrider-Ladys von L.A. (360° - GEO Reportage) [3ql7jtqylzU].mp4
_new/Die Magellan-Lotsen (360° - GEO Reportage) [zJXstWpax9g].mp4
_new/Die Marmorberge von Italien (360° - GEO Reportage) [bND3Vz0DIb8].mp4
_new/Die Meerfrauen von Japan (360° - GEO Reportage) [7Xh5pUZt0yM].mp4
_new/Die Millionen-Dollar-Hirsche (360° - GEO Reportage) [b96BcyI9T9M].mp4
_new/Die Minenratten von Tansania (360° - GEO Reportage) [BYPBaBKHjpM].mp4
_new/Die Minga - Umzug auf Chilenisch (360° - GEO Reportage) [H8MxGlRHRHA].mp4
_new/Die Mutter der Bonobos (360° - GEO Reportage) [GoiCEwbQxA0].mp4
_new/Die Narzisseninsel vor Cornwall (360° - GEO Reportage) [2k8K6kPY24U].mp4
_new/Die neuen Nomaden von Kirgisistan (360° - GEO Reportage) [V5qvHh2phPw].mp4
_new/Die Odyssee der Mönchsrobbe (360° - GEO Reportage) [IrOfUxc812k].mp4
_new/Die Oldtimer von Curaçao (360° - GEO Reportage) [RjuudARpaEQ].mp4
_new/Die Ostsee, Sehnsuchtsort der Kraniche (360° - GEO Reportage) [p-f4YVXnycM].mp4
_new/Die Polarbahn (360° - GEO Reportage) [VJ6JS8MWo9Y].mp4
_new/Die Polarschule der Nomadenkinder (360° - GEO Reportage) [pAB_SIM2Big].mp4
_new/Die Puppen tanzen! Litauens rollendes Theater (360° - GEO Reportage) [axKuA1qBWGQ].mp4
_new/Die rasenden Engel der Línea 5 (360° - GEO Reportage) [svJ9c2nluQ4].mp4
_new/Die Rettungshunde vom Gardasee (360° - GEO Reportage) [Xqj1OOEq5M4].mp4
_new/Die Samurai von Fukushima (360° - GEO Reportage) [jVgE3nypw-c].mp4
_new/Die Sandmenschen von Schoina (360° - GEO Reportage) [EdPZhBjtBas].mp4
_new/Die scharfen Klingen der Auvergne (360° - GEO Reportage) [Zo2vsTRz4x0].mp4
_new/Die Schlammfußballer von Island (360° - GEO Reportage) [jJRGSboanao].mp4
_new/Die schwebenden Särge von Georgien (360° - GEO Reportage) [-2OmrWF4YiQ].mp4
_new/Die Schwestern der Erde (360° - GEO Reportage) [nfNQ5wCTWlQ].mp4
_new/Die schwimmenden Dörfer der Ha Long Bucht (360° - GEO Reportage) [At-Ei18eK_8].mp4
_new/Die Spinnenjäger von Venezuela (360° - GEO Reportage) [wjmhUyOUGvc].mp4
_new/Die Tangospelunken von Buenos Aires (360° - GEO Reportage) [gPgur58gJIc].mp4
_new/Die Teebahn von Darjeeling (360° - GEO Reportage) [htD-vlXaVcw].mp4
_new/Die Todesküste von Galicien (360° - GEO Reportage) [MMsnMfaXpUA].mp4
_new/Die Trommler von Burundi (360° - GEO Reportage) [jgIQx6w8oN8].mp4
_new/Die verrückten Karren des Mister Winfield (360° - GEO Reportage) [Vg9aMMkF7PQ].mp4
_new/Die versunkenen Flugzeuge (360° - GEO Reportage) [2wbl4SWQ3q8].mp4
_new/Die Verwandlungskünstler von Dakar (360° - GEO Reportage) [jjnY-79AN_s].mp4
_new/Die Vespa-Rebellen in Indonesien (360° - GEO Reportage) [T882pntN-Jo].mp4
_new/Die Waldbahn der Karpaten (360° - GEO Reportage) [oglBMMjahqg].mp4
_new/Die Wassernomaden vom Sambesi (360° - GEO Reportage) [f0lmD4C0Vs0].mp4
_new/Die Windreiter der Anden (360° - GEO Reportage) [xkVql_Bm6FM].mp4
_new/Die Zedernuss, die Königin von Sibirien (360° - GEO Reportage) [0kvHCK0011o].mp4
_new/Ein Baumhaus in Costa Rica (360° - GEO Reportage) [JL3N7pLoXFM].mp4
_new/Ein Dorfladen reist durch Lettland (360° - GEO Reportage) [wHc_aS93aZc].mp4
_new/Ein Traum von Schokolade (360° - GEO Reportage) [BxUtrDZX1FI].mp4
_new/Eine Fähre nach Afrika (360° - GEO Reportage) [GwUd8KDdUN4].mp4
_new/Eine zweite Art von Frau – Thailand, das Dritte Geschlecht (360° - GEO Reportage) [h2o97Qd26oI].mp4
_new/Eishockey, Mädchentraum im Himalaja (360° - GEO Reportage) [ksF9UzJGXeE].mp4
_new/Elbsandsteingebirge - Märchenwelt und Meisterwerke (360° - GEO Reportage) [PEJoGOk3veQ].mp4
_new/Eremitage - Palast der Katzen (360° - GEO Reportage) [_hiU5OzkNQ0].mp4
_new/Eritrea - Ein Esel für die Zukunft (360° - GEO Reportage) [deTDbCTBKtA].mp4
_new/Escobars Erbe - Kolumbiens Kokain-Hippos (360° - GEO Reportage) [T8zWiccuv0w].mp4
_new/Esmeraldas Edelkakao (360° - GEO Reportage) [IMVYBpL-z4E].mp4
_new/Estland und das kleine Königreich der Seto (360° - GEO Reportage) [zgv8oZfn-Sk].mp4
_new/Estland, Krötenretter im Einsatz (ARTE 360° Reportage) [xzfFqvblS34].mp4
_new/Europas Urwälder - Ein Schatz der Natur (360° - GEO Reportage) [JXN5lNsTZCI].mp4
_new/Falklandinseln - Pinguine auf dem Vormarsch (360° - GEO Reportage) [A_eZDMVKVco].mp4
_new/Faszination Elbrus - der Ritt zum Gipfel (360° - GEO Reportage) [FgNR3JW-QbE].mp4
_new/Federn, Falten, Seidenblumen - Die Geheimnisse der Haute Couture (360° - GEO Reportage) [2MTSdkn22a4].mp4
_new/Finnland, die rasenden Schrottkisten (360° - GEO Reportage) [AR9cNhlECyA].mp4
_new/Florenz, Fußball bis aufs Blut (360° - GEO Reportage) [dpdeqdga-RM].mp4
_new/Florida, Invasion der Pythons (360° - GEO Reportage) [VMQIqDPSNHw].mp4
_new/Fort McMurray, Kanada im Ölfieber (360° - GEO Reportage) [eadcv_oMM9o].mp4
_new/Frankreichs Winzer - Tradition trifft Passion (360° - GEO Reportage) [pQaBkRIgRk0].mp4
_new/Fremdenlegion, die Hölle im Regenwald (360° - GEO Reportage) [p3uxoko70Cc].mp4
_new/Friaul, Benvenuti im Musiktal (360° - GEO Reportage) [_-7XZj09-A0].mp4
_new/Frisch vermählt in Estland (360° - GEO Reportage) [OzL34KdYfLM].mp4
_new/Ganz ritterlich - Kastiliens Kämpfer (360° - GEO Reportage) [wZgpqRaV7Ik].mp4
_new/Georgien, die Wiege des Weins (360° - GEO Reportage) [iSex9SfaNDg].mp4
_new/Gletscherflieger – Faszination in Weiß (360° - GEO Reportage) [jEZT_6_qloo].mp4
_new/Gnadenhof ＂Gut Aiderbichl＂ (360° - GEO Reportage) [LkOdAquYeZQ].mp4
_new/Goldrausch in Sibirien (360° - GEO Reportage) [orPQ74toO10].mp4
_new/Griechenland, Aufbruch am Olymp (360° - GEO Reportage) [6pWfTh6Y4-o].mp4
_new/Großglockner, König der Hochalpen (360° - GEO Reportage) [7SZoha01QG0].mp4
_new/Guano - Schatzinseln und Vogeldreck (360° - GEO Reportage) [hDbmGter130].mp4
_new/Hai-Alarm in Polynesien (360° - GEO Reportage) [kwuqkmG7z_M].mp4
_new/Hamburg - Welthafen mit schwimmender Kirche (360° - GEO Reportage) [p43Ug9kO7WQ].mp4
_new/Hamburg, die Stadt der Schwäne (360° - GEO Reportage) [f1K7nBVO7Lk].mp4
_new/Harpyien, die größten Greifvögel des Regenwaldes (360° - GEO Reportage) [rpnZILRBjaw].mp4
_new/Hawaii, Beachboys auf Patrouille (360° - GEO Reportage) [7NHpb3KDYH0].mp4
_new/Heilende Schwingungen der Klangschalen (360° - GEO Reportage) [0JQRSU8Gzc0].mp4
_new/Hexenwahn in Tansania (360° - GEO Reportage) [8K_unhDEPJo].mp4
_new/Highway durch die Arktis (360° - GEO Reportage) [dx2YI4of1wU].mp4
_new/Hinter den Kulissen von Venedig (360° - GEO Reportage) [nuuE8tS-bDo].mp4
_new/Hochzeit auf neapolitanisch (360° - GEO Reportage) [tuCZYYFJHLM].mp4
_new/Honeymoon auf Hainan (360° - GEO Reportage) [WUwS5Yac1PY].mp4
_new/Huskies am Start! (360° - GEO Reportage) [3XyG82_dG-0].mp4
_new/Idjwi - Afrikas vergessene Insel (360° - GEO Reportage) [y_zW09TMKaQ].mp4
_new/Im Land der Schwarzen Witwen (360° - GEO Reportage) [TwJc0Qx152o].mp4
_new/In acht Meilen um die Welt (360° - GEO Reportage) [t59ghH7Ant8].mp4
_new/In den Smaragdbergen von Bahia (360° - GEO Reportage) [hjMe94sQCRk].mp4
_new/Indien - Das Geschäft mit dem Tempelhaar (360° - GEO Reportage) [Ka5if339los].mp4
_new/Indien - Kampf den Scharlatanen (ARTE 360° Reportage) [-Clpkb3JdkI].mp4
_new/Indien, das größte Schulessen der Welt (360° - GEO Reportage) [K7E2T9Imdok].mp4
_new/Indien, heilendes Ayurveda (360° - GEO Reportage) [EqHxC_ym5uA].mp4
_new/Indiens Dschungelbuchklinik (360° - GEO Reportage) [Tc7yml23q14].mp4
_new/Indiens jüngste Polizisten (360° - GEO Reportage) [czIONbtfL-I].mp4
_new/Indiens Kurkuma - Heilsam und heilig (360° - GEO Reportage) [Qx7wwbJDDdE].mp4
_new/Insekten, unser Speiseplan für morgen？ (360° - GEO Reportage) [OOxmAapp8vY].mp4
_new/Iquitos, Regenwaldmetropole am Amazonas (360° - GEO Reportage) [zRCocBSf_SI].mp4
_new/Island - Der große Schafabtrieb (360° - GEO Reportage) [2tbQzv7Mnqk].mp4
_new/Island, Leben auf dem Pulverfass (360° - GEO Reportage) [n97-kFfr0xg].mp4
_new/Island, von strickenden Männern und Pullovern (360° - GEO Reportage) [4lAHP0Q8908].mp4
_new/Italien, eine neue Glocke für Monopoli (360° - GEO Reportage) [FLTObV0M5RE].mp4
_new/Italiens Kapern - Der Geschmack des Südens (360° - GEO Reportage) [wriortwg56E].mp4
_new/Jadehandel im Goldenen Dreieck (360° - GEO Reportage) [grEeTdeih0Q].mp4
_new/Japan, der Meister des Zen-Gartens (360° - GEO Reportage) [CA-DwIr8lA4].mp4
_new/Java, zauberhaftes Schattentheater (360° - GEO Reportage) [HE8MAIiX9OU].mp4
_new/Jemens verschleierte Zukunft (360° - GEO Reportage) [gCIzyjixKpI].mp4
_new/Jenny und ihre Flughunde (360° - GEO Reportage) [P81A8ljYhNM].mp4
_new/Jerusalem im Morgengrauen (360° - GEO Reportage) [XeHZ3UW7woE].mp4
_new/Jillaroos - Cowgirls im australischen Outback (360° - GEO Reportage) [dzNcn7hvzAc].mp4
_new/Joaquims wilde Reiter (360° - GEO Reportage) [CU4ljdc9mNs].mp4
_new/Johana - Make-up und Motorenöl (360° - GEO Reportage) [t3FempEGGaw].mp4
_new/Johannesburg – Eine Stadt macht dicht (360° - GEO Reportage) [CyD4tnGwcxs].mp4
_new/Jordanien, Dynastie der Pferde (360° - GEO Reportage) [CTbgWjUewgA].mp4
_new/Kalifornien auf die harte Tour (360° - GEO Reportage) [qIx8uIMxDIM].mp4
_new/Kalkstein - Das weiße Gold von Brac (360° - GEO Reportage) [sx5ieaeHnUs].mp4
_new/Kalmückien, Die Rückkehr der Mönche (360° - GEO Reportage) [8f4nujAr3Uc].mp4
_new/Kambodscha - Die Seele der Seide (360° - GEO Reportage) [ZWSMXpf-EQc].mp4
_new/Kambodscha, Ratte süß-sauer (360° - GEO Reportage) [Fadu9DpauSQ].mp4
_new/Kambodscha, Sithas große Waisenfamilie (360° - GEO Reportage) [dFjDEa-tVVI].mp4
_new/Kamelmilch, Kasachstans Wundermedizin (360° - GEO Reportage) [5JYKH97ayxI].mp4
_new/Kamtschatka, kochende Erde (360° - GEO Reportage) [9Nbz_igMCmM].mp4
_new/Kanada - Mit der Hebamme durch die Badlands (360° - GEO Reportage) [Gdcj-iqqRs8].mp4
_new/Kanada, Indianer schreiben Geschichte (360° - GEO Reportage) [f1L930_UNW0].mp4
_new/Kanadas Buschpiloten im Einsatz (360° - GEO Reportage) [dr7OQ8XcdXA].mp4
_new/Kastanien, das Brot der Korsen (360° - GEO Reportage) [PZIIed051OE].mp4
_new/Kaviar - Der Schatz aus dem Iran (360° - GEO Reportage) [i8lc_XQujbM].mp4
_new/Kaviar, das schwarze Gold Italiens (360° - GEO Reportage) [Opg00LWco4s].mp4
_new/Kenia - Das Dorf der Frauen (360° - GEO Reportage) [CGJ9nKH4zFw].mp4
_new/Kenias Spürhunde - Rettung für die Elefanten (360° - GEO Reportage) [MY6baZRwEL8].mp4
_new/Kentucky - Die Schlacht von Sacramento (360° - GEO Reportage) [BM7Tyu59rrI].mp4
_new/Koh Panyee - Thailands fußballverrückte Insel (360° - GEO Reportage) [RC_j7QQ1r5U].mp4
_new/Kolumbien - Ein Riesenrad auf Reisen (360° - GEO Reportage) [l0tgOGBbI7M].mp4
_new/Kolumbien, DC3-Oldtimer versorgen den Regenwald (360° - GEO Reportage) [VqPIqn1upqs].mp4
_new/Königliche Mounties - Kanadas berittene Polizei (360° - GEO Reportage) [MKnpMHIWWSI].mp4
_new/Kourou： Palmen, Raketen, Gefängnisinseln (ARTE 360° Reportage) [LckZ2_Lw88E].mp4
_new/Kreta - Die süßen Früchte des Johannisbrotbaums (360° - GEO Reportage) [rVaOPVPAC5Y].mp4
_new/Kuba, der Dreh mit der Orgel (360° - GEO Reportage) [tnpfneRKHxY].mp4
_new/Kuba, eine Generation im Wandel (360° - GEO Reportage) [uONkvisdPJo].mp4
_new/Kung Fu - Chinas neue Kämpferinnen (360° - GEO Reportage) [rzkqoL0_cEw].mp4
_new/Kurt und seine Wölfe (360° - GEO Reportage) [Khp3kDHWSdo].mp4
_new/Kyuchu - Wo Japans grüner Tee wächst (360° - GEO Reportage) [EoXyDIckuRI].mp4
_new/Laetitia, allein unter Wölfen (360° - GEO Reportage) [r5sfDn03OWw].mp4
_new/Lamu, die Insel der Esel (360° - GEO Reportage) [Z8Xny07TdXQ].mp4
_new/Lappland, Rushhour im hohen Norden (360° - GEO Reportage) [MT5oNZ0Y6JY].mp4
_new/Las Fallas - Valencias feurige Fiesta (ARTE 360° Reportage) [ug2XFpN43CU].mp4
_new/Legende auf Schienen - Skandinaviens Kirunabahn (360° - GEO Reportage) [mGdgh-eQVM4].mp4
_new/Lettland, das Land der Sänger (360° - GEO Reportage) [F7ljNcCsIhA].mp4
_new/Lichterglanz im Norden - Winter in Stockholm und den Schären (360° - GEO Reportage) [uE8XcPEKQIo].mp4
_new/Louisiana - Land unter bei den Shrimpfischern (360° - GEO Reportage) [tS_0NFzr2l4].mp4
_new/Lust auf Liebe in Lisdoonvarna (360° - GEO Reportage) [MlM93JHkIU4].mp4
_new/Majuli, ein Inselvolk trotzt den Fluten (360° - GEO Reportage) [ZKUYH2GJDpM].mp4
_new/Malaysia, von Frauen und Motorrädern (360° - GEO Reportage) [yvXaWlw37fQ].mp4
_new/Marokko, die andere Seite des Paradieses (360° - GEO Reportage) [ATAr5oY041c].mp4
_new/Marseille, kopfüber ins Blau (360° - GEO Reportage) [sVXtF-PwPQY].mp4
_new/Mate-Tee, die Seele Argentiniens (360° - GEO Reportage) [fWvRJ-pbYxI].mp4
_new/Mauretanien - Aufstand der Fischerfrauen (360° - GEO Reportage) [eRzhzWVRgns].mp4
_new/Mecaniqueros - Nichts ist unmöglich in Havanna (360° - GEO Reportage) [80vkFm7tzCM].mp4
_new/Mezcal, Hochprozentiges aus Mexiko (360° - GEO Reportage) [bpjZIo4bmGw].mp4
_new/Mit dem Wanderbarden durch Aserbaidschan (360° - GEO Reportage) [ikwsm25rULY].mp4
_new/Mit der Lok durch Angola (360° - GEO Reportage) [jbkp_3nRDjQ].mp4
_new/Mit Tempo und Leidenschaft： Argentiniens Polo-Spielerinnen (ARTE 360° Reportage) [Y-eQibAkbmo].mp4
_new/Mit Volldampf durch Kärnten (360° - GEO Reportage) [0HrxXJsDky4].mp4
_new/Miyako, Insel des langen Lebens (360° - GEO Reportage) [04TrtARWfGA].mp4
_new/Modelsuche in Sibirien (360° - GEO Reportage) [ketqT7focbQ].mp4
_new/Mohair, das Garn der guten Hoffnung (360° - GEO Reportage) [NDsFCWIqsIk].mp4
_new/Mustang - Flucht aus den Bergen (360° - GEO Reportage) [3ti-NbruVhU].mp4
_new/Myanmar - Per Zug durch die Zeit (360° - GEO Reportage) [Rj3NNtFqAjo].mp4
_new/Myanmar, die Marmorkünstler von Mandalay (360° - GEO Reportage) [iV3arcWLL-s].mp4
_new/Myanmar, ein Dorf braucht Strom (360° - GEO Reportage) [vN4snehmVSk].mp4
_new/Myanmars Bambusbrücke - Ein Dorf packt an (360° - GEO Reportage) [Mx0SpmGP9JM].mp4
_new/Namibias Geparden - Hoffnung für die Raubkatzen (360° - GEO Reportage) [s9UPirsiFbA].mp4
_new/Nepal - Die Krieger vom Dach der Welt (360° - GEO Reportage) [m-7u2kAG2DQ].mp4
_new/Neuseelands Lauf der Extreme (360° - GEO Reportage) [6TSXVJB4nmQ].mp4
_new/New York - Die kleinste Oper der Welt (360° - GEO Reportage) [I-VACV5HkOs].mp4
_new/Nicaragua - Fluch der Langustentaucher (360° - GEO Reportage) [bO6BiCVyGug].mp4
_new/Nopal, der Alleskönner aus Mexiko (ARTE 360° Reportage) [MkXx_8rac_M].mp4
_new/Norwegen, Försterinnen auf dem Vormarsch (360° - GEO Reportage) [Vge_eMlIxEY].mp4
_new/Notruf Nordseeküste - Die Robben-Retter (360° - GEO Reportage) [ltSG2rftqu8].mp4
_new/Oman - Die Rosen der Wüste (360° - GEO Reportage) [LwijL77IF3c].mp4
_new/Paco Pacos – Die Knatterkisten vom Amazonas (360° - GEO Reportage) [SWt30v35IdA].mp4
_new/Palawan, das Dorf der Gefangenen (360° - GEO Reportage) [dH7ls3Lqtzw].mp4
_new/Panzer, Wölfe, Rothirsche - Bayerns wilder Übungsplatz (360° - GEO Reportage) [kyrHUKDiyck].mp4
_new/Paraguays neue Häuser (360° - GEO Reportage) [quHXX9_bIjQ].mp4
_new/Paris, Blitz Motorcycles (360° - GEO Reportage) [RcPiWMzimBk].mp4
_new/Pelikane, die Könige des Donaudeltas (360° - GEO Reportage) [ZgBcESvfvYA].mp4
_new/Percheron - Das Kraftpaket mit einer Pferdestärke (360° - GEO Reportage) [fr7QjYkoqf0].mp4
_new/Peru - Delfine in Gefahr (360° - GEO Reportage) [LmSo7bINHXQ].mp4
_new/Peru, ein Alpaka für Christobal (360° - GEO Reportage) [u27JvFwOKn0].mp4
_new/Philippinen - Rendezvous mit einem Adler (360° - GEO Reportage) [Qr9EvRRTYLo].mp4
_new/Polen - Ärger im Revier (360° - GEO Reportage) [YMQMvv9gl4A].mp4
_new/Polen, Winter in den Waldkarpaten (360° - GEO Reportage) [tRxGlm8BqbY].mp4
_new/Postbote im Himalaya (360° - GEO Reportage) [VHEpd2C1GvQ].mp4
_new/Puerto Rico - Ein Krankenhaus für Seekühe (360° - GEO Reportage) [B2ODRBt1BTI].mp4
_new/Pyrenäen, ein Hirte zwischen Himmel und Erde (360° - GEO Reportage) [hxPBgj2j_eg].mp4
_new/Radio Patagonia (360° - GEO Reportage) [xWorOwWPUMg].mp4
_new/Rattenjagd im Südpolarmeer (360° - GEO Reportage) [oGcMkh67AeE].mp4
_new/Razzia im Regenwald (360° - GEO Reportage) [ExA03zKchVc].mp4
_new/Ring frei für Sambias Boxerinnen (360° - GEO Reportage) [MmBs2InkDl0].mp4
_new/Rio - Vom Strich auf den Laufsteg (360° - GEO Reportage) [lONevE9h_GM].mp4
_new/Río de la Plata - SOS am Silberfluss (360° - GEO Reportage) [IkMvsCA4uo0].mp4
_new/Rom - Das Leben der Komparsen (360° - GEO Reportage) [-M2Nf4GPbHg].mp4
_new/Rosa Amélia - Fischer, Freunde, Fado (360° - GEO Reportage) [t9HMH3k3Rz0].mp4
_new/Ruanda - Land der Frauen (360° - GEO Reportage) [cgNXNRjbB8E].mp4
_new/Rum auf Guadeloupe (360° - GEO Reportage) [9N1Qll5w0ng].mp4
_new/Rumänien, eine Weihnachtsreise ins Donaudelta (360° - GEO Reportage) [pcjXQq5fnx4].mp4
_new/Russlands Zirkusschule auf Tour (360° - GEO Reportage) [5dS2nHbEqsM].mp4
_new/Saint Pierre und Miquelon - Archipel in der Isolation (360° - GEO Reportage) [z6mots9SAg0].mkv
_new/Saint Pierre und Miquelon - Archipel in der Isolation (360° - GEO Reportage) [z6mots9SAg0].mp4
_new/Sansibars erstes Frauenorchester (360° - GEO Reportage) [PXO6rKXlfnk].mp4
_new/Saphir-Fieber auf Madagaskar (360° - GEO Reportage) [gSR8zp3hLgQ].mp4
_new/Sardinien, Stolz und Ehre hoch zu Ross (360° - GEO Reportage) [JlaZDPOEupE].mp4
_new/Sark, die Kanalinsel der Queen (360° - GEO Reportage) [ybpV9JWD6qs].mp4
_new/Schignano, ein uralter Karneval in Italiens Bergen (360° - GEO Reportage) [UBhl_XT1ixY].mp4
_new/Schottland - Kampf, Clan und Königin (360° - GEO Reportage) [AO5mzpVh6PI].mp4
_new/Schottland, die Seenotretter der Orkney Islands (360° - GEO Reportage) [qzTYfQqZltc].mp4
_new/Schweiz, das Verschwinden der Gletscher (360° - GEO Reportage) [QNabMUFSr2Y].mp4
_new/Schwerelos im Windkanal (360° - GEO Reportage) [jp5BDv9KCzY].mp4
_new/Shetland, das Ende des Öls (360° - GEO Reportage) [ReBwYDvW-VM].mp4
_new/Sibirien, der Kapitän und die Lena (360° - GEO Reportage) [7g-j259KxH0].mp4
_new/Sibirien, die Eisschneider von Jakutsk (360° - GEO Reportage) [_pzMXsISUPU].mp4
_new/Sibirien, die Polarstraße ins Polarmeer (360° - GEO Reportage) [S7VcirrE2xc].mp4
_new/Sikkim, das alte Wissen der Schamanen (360° - GEO Reportage) [DW5ajV0yaFw].mp4
_new/Singvögel - Die goldenen Stimmen von Singapur (360° - GEO Reportage) [nqHruOs-dqE].mp4
_new/Slab City, wildes Leben in der Wüste (360° - GEO Reportage) [T0K8Qv0eupI].mp4
_new/Slowenien, Land des Honigs (360° - GEO Reportage) [QxhQbpP57PM].mp4
_new/So schmeckt Australien! (360° - GEO Reportage) [G_gFhibEvNA].mp4
_new/Sokotra, Schatzinsel in Gefahr (360° - GEO Reportage) [G-TbiXRVLTM].mp4
_new/SOS in den Rocky Mountains (360° - GEO Reportage) [S3N8fPmBOD0].mp4
_new/Spitzbergen, eisige Insel (360° - GEO Reportage) [5WVk0CvsUA0].mp4
_new/Spreewald - Kähne, Köche, Klapperstörche (360° - GEO Reportage) [FFHcOUH17TE].mp4
_new/Sri Lanka - Eine legendäre Eisenbahnstrecke (360° - GEO Reportage) [ldpHfqDbWHQ].mp4
_new/St. Bernhard - Von Menschen und Hunden (360° - GEO Reportage) [UBQ1XhTzHic].mp4
_new/St. Helena, vergessen im Atlantik (360° - GEO Reportage) [srGhZLAIPCk].mp4
_new/Stilikone Panamahut (360° - GEO Reportage) [FLkf0zJdhFY].mp4
_new/Stromboli, zwischen Feuer und Meer (360° - GEO Reportage) [_z29qS0mTjY].mp4
_new/Südkoreas magische Tempelküche (360° - GEO Reportage) [if6OhSEjkxM].mp4
_new/Sulawesi - Die letzten Seenomaden (360° - GEO Reportage) [5ZSLl8Wj_-E].mp4
_new/Sumatra - Ettis Schönheitssalon (360° - GEO Reportage) [0JguIiABfw8].mp4
_new/Sumatras letzte Orang-Utans (360° - GEO Reportage) [1l8k6nfu5NQ].mp4
_new/Svanetien - Von Lebenden und Toten (360° - GEO Reportage) [KZ9v7YAJzR8].mp4
_new/Taipan die gefährlichste Schlange der Welt (360° - GEO Reportage) [ItZXECu1GPQ].mp4
_new/Taipeh 101 - Der Himmel über Taiwan (360° - GEO Reportage) [SJKNUloS0O4].mp4
_new/Taiwan - Fliegende Fische oder Atommüll？ (360° - GEO Reportage) [Uz7hFkRtHb4].mp4
_new/Tanganjikasee, vom Kanonenboot zum Passagierschiff (360° - GEO Reportage) [d9sb8TpPhtE].mp4
_new/Tapire - Die Dschungel-Gärtner (360° - GEO Reportage) [bQXxzQjmPvo].mp4
_new/Tasmanien - Wächterin im Paradies (360° - GEO Reportage) [df1G1ZN2OdM].mp4
_new/Tasmanien, Sympathie für den Teufel (360° - GEO Reportage) [iXgcWz3Dqh0].mp4
_new/Thailand - Kinder im Ring (360° - GEO Reportage) [LtDq72ui27g].mp4
_new/Thailand, Raketen für die Götter (360° - GEO Reportage) [HPDrBToxk24].mp4
_new/Thailands Elefanten - raus aus der Stadt! (360° - GEO Reportage) [m3qxxeiI04M].mp4
_new/Tonga, Paradies der Südsee？ (360° - GEO Reportage) [a6-2aXuDLTw].mp4
_new/Tradition am Steilhang - Die Schweiz und ihre Wildheuer (360° - GEO Reportage) [FsESCsAehtk].mp4
_new/Traumberuf Schäfer (360° - GEO Reportage) [J6auo5M-mxI].mp4
_new/Tunesien, die Kunst der Berbertattoos (360° - GEO Reportage) [0fWMiz2aS_o].mp4
_new/Tunesien, die Suche nach dem Tintenfisch (360° - GEO Reportage) [K--aZyNB-LQ].mp4
_new/Überleben am Manila Express (360° - GEO Reportage) [0uMJ3IZ2_FI].mp4
_new/Uganda - Der Weg zum Fahrradtaxi (360° - GEO Reportage) [Z-9fqoYchv4].mp4
_new/Unter Haien： Riffpatrouille in der Sulu-See (360° - GEO Reportage) [zDVgKjAc8A0].mp4
_new/Unterwegs mit der Irish Coast Guard (360° - GEO Reportage) [vdqig1_VkIg].mp4
_new/Vagabunden der Wüste Gobi (360° - GEO Reportage) [TYNNyF65mvY].mp4
_new/Valparaiso, die Stadt der Aufzüge (360° - GEO Reportage) [VZw_EvXbp18].mp4
_new/Venezuela - Die alte Frau und das Meer (360° - GEO Reportage) [sOtopRXixzg].mp4
_new/Venezuela, die Blitze von Catatumbo (360° - GEO Reportage) [AVB38wERs3Q].mp4
_new/Vietnam, das Schicksal der Mondbären (360° - GEO Reportage) [bcv3VsOTMdo].mp4
_new/Vietnam, die letzten Pangoline (360° - GEO Reportage) [HXALW-m2RxM].mp4
_new/Vietnam, Kobra auf dem Teller (360° - GEO Reportage) [k5mRGmiLhBA].mp4
_new/Vietnams vermintes Paradies (360° - GEO Reportage) [56EQyMDFfzM].mp4
_new/Vom Klassenzimmer in die Kalahari (360° - GEO Reportage) [AB2q4v0rlYo].mp4
_new/Von Männern und Mustangs (360° - GEO Reportage) [vEQecvaogb8].mp4
_new/Weltmeister auf vier Pfoten (360° - GEO Reportage) [B0wdXJ_U7TY].mp4
_new/Wenzhou, die Schuh-Stadt von China (360° - GEO Reportage) [BlMBuBYO0IQ].mp4
_new/Wilde Pferde im Donaudelta  (360° - GEO Reportage) [nfDk1G85yUA].mp4
_new/Wilde Schweiz - Von Ringern und Schwingern (360° - GEO Reportage) [BOZJeflZbeM].mp4
_new/Wilde Waterkant - Nordfriesland und seine Gänse (360° - GEO Reportage) [p33T3S0tqBA].mp4
_new/Wildererjagd am Mount Kenya (360° - GEO Reportage) [UAGR4vE_i0U].mp4
_new/Yoga, Indiens erstaunliche Medizin (360° - GEO Reportage) [uae6n-lyViY].mp4
_new/Zauberhafte Mosel (360° - GEO Reportage) [fHHJoYzQuz8].mp4
s01/s01e01 Beirut – die Milliarden-Dollar-Utopie (1999) (YT E_uSFyHf7BM).mp4
s01/s01e02 Chandigarh – Leben im Beton (YT FGgrN8pRhTU).mp4
s01/s01e03 Brasilia Metropole vom Reißbrett (YT _7Y2Y4bbw9s).mp4
s01/s01e04 Celebration Leben in Harmonie (YT cA7vQS4fCTI).mp4
s01/s01e05 Die mächtigen Frauen von Juchitán (YT 1mSDukDzpDM).mp4
s01/s01e06 Hazeras Geschäfte (YT R5rvxs4hX20).mp4
s01/s01e07 Die neue Kunst des Kinderkriegens (YT LrC1AVBi3c4).mp4
s01/s01e08 Der kleine Unterschied im Kopf (YT cwkotpcPnSw).mp4
s01/s01e09 Die Spurensucher (YT Lo0nKPEQ8Rw).mp4
s01/s01e10 Auf dem Holzweg (YT _dmzJgBbZQ4).mp4
s01/s01e10 Auf dem Holzweg (YT XAyYoAetjuQ).mp4
s01/s01e11 Heilkraft aus dem Urwald (YT NrEukDOS1EA).mp4
s01/s01e12 Die Pille für den Wald (YT dLFIQxBpprQ).mp4
s01/s01e13 Copyright Natur (YT tCbl1P76mxs).mp4
s01/s01e14 Mensch Roboter! (YT vqEw-I_qCfU).mp4
s01/s01e15 ABC des Universums (YT rCzm-aVuTzg).mp4
s01/s01e16 Die Erfindung der Wirklichkeit (YT 06CDuq1PtKo).mp4
s01/s01e17 Der Markt der Schönheit (YT TNonjmeywIQ).mp4
s01/s01e18 Cuba Von der stillen Revolte der Schönheit (YT YKZbpc4kuSI).mp4
s01/s01e19 Das Maß der Schönheit (YT LpKB8n-ejwk).mkv
s01/s01e19 Das Maß der Schönheit (YT XW4c4rXmj_U).mkv
s01/s01e20 Die andere Seite der Schönheit (YT tcYPNiXisX0).mp4
s01/s01e21 Geniale Störenfriede (YT 9N_DwJ2fymM).mp4
s01/s01e22 Musik macht klug (YT GdWPt-utQPM).mp4
s01/s01e23 Think Tank Die Schule der Affen (YT P6QzAbgbxFg).mp4
s01/s01e24 Künstliche Intelligenz (YT 3rC25gW3xxk).mp4
s01/s01e25 Der Kaninchen-Krieg (YT jYrt-OPNDJM).mp4
s01/s01e26 Countdown ins Desaster (YT Re2So-kXO2E).mkv
s01/s01e27 Liebe und andere Katastrophen (YT WgWcbKnYJJY).mp4
s01/s01e28 Verkehrte Sicherheit (YT G1M3FDyey0k).mp4
s01/s01e29 Die Meister des Glücks (YT 1U3Bl34Iu3A).mp4
s01/s01e30 Die Macht des Lachens (YT TCOpr5a6tAY).mp4
s01/s01e31 Chemie der Traurigkeit (YT 1SVM-x4U7w4).mp4
s01/s01e32 Inseln der Glücklichsten (YT 0ejrRWcXiro).mp4
s01/s01e33 Hunger nach Sonne (YT WicPXmsDRC8).mp4
s01/s01e34 Die Leuchtkraft der Natur (YT 7_3cDZ3yVrg).mp4
s01/s01e34 Die Leuchtkraft der Natur (YT epuV5ouQ7OA).mp4
s01/s01e35 Die Seele des Lichts (YT DniKsVQuah0).mp4
s01/s01e35 Die Seele des Lichts (YT gFoyqUu_hAU).mkv
s01/s01e36 Lichtkunst Kunstlicht (YT FU3uG3sr75w).mp4
s01/s01e37 Eine Liebe auf Bali (YT hxAERStQV4w).mp4
s01/s01e37 Eine Liebe auf Bali (YT kf8zhso0u4s).mkv
s01/s01e38 Mythos Mutterliebe (YT mgGI3er1qPI).mp4
s01/s01e39 Angst macht verführerisch (YT c238XngnQas).mkv
s01/s01e39 Angst macht verführerisch (YT YPsAb0uUOyA).mp4
s01/s01e40 Menü der Zärtlichkeit (YT cgu64PhWtA8).mkv
s01/s01e40 Menü der Zärtlichkeit (YT r0rtNVYxUkg).mp4
s02/s02e01 Ernstfall Erdbeben (YT MXBz7QnU3Po).mp4
s02/s02e02 Im Schatten des Vulkans (YT VGLT3ZeQwR0).mkv
s02/s02e03 Operation Wolkenbruch (YT IjEjPOMZoGk).mp4
s02/s02e04 Tsunami Die tödliche Welle (YT DUxn9Li2rcU).mp4
s02/s02e05 Casino der Häuptlinge (YT aONYl3VUqW4).mp4
s02/s02e06 Schach Krieg auf 64 Feldern (YT DHhe-fv1P_o).mkv
s02/s02e07 Mehr als ein Kinderspiel (YT KXkwwZ_o6n0).mp4
s02/s02e08 Spielplatz Natur (YT 6XpJnxWkHnU).mp4
s02/s02e09 Beruf Grabräuber (YT lpcnsH66igQ).mp4
s02/s02e10 Schätze aus dem All (YT auISYpA2psM).mp4
s02/s02e10 Schätze aus dem All (YT W_s6Qhvwh7Q).mkv
s02/s02e11 Die Taucher der Goldküste (YT Jsm-8wxKxDo).mp4
s02/s02e12 Im Bann der Rubine (YT hYYAObzGdVs).mp4
s02/s02e13 Die Klinik der Schamanen (YT BsUR1lHoDNA).mkv
s02/s02e14 Organe nach Maß (YT unxzp52RP0c).mkv
s02/s02e15 Die Jäger des Lassa-Virus (YT 8ALpHNqxoL0).mp4
s02/s02e16 Chirurgen am Joystick (YT GlPBNbgtNpE).mp4
s02/s02e17 Die High-Tech Polizei (YT -82yroKn9C8).mkv
s02/s02e17 Die High-Tech-Polizei (YT OeQIgSeBN5k).mp4
s02/s02e18 Die Kunst des Fälschens (YT CuJOick2_ZY).mkv
s02/s02e19 Geheimnisse der Toten (YT bA5xe1HPaLw).mkv
s02/s02e20 Psycho-Detektive (YT 8yaQbw9XjbQ).mp4
s02/s02e21 Das Fenster zum Meer (YT 0QK0oUCiGSk).mp4
s02/s02e21 Das Fenster zum Meer (YT pr77EnZFwug).mp4
s02/s02e22 Schwarze Brandung (YT MQNTxheCFSw).mp4
s02/s02e23 Durst nach Meer (YT WAjs-VrhFNs).mp4
s02/s02e24 SOS auf hoher See (YT qVKSXlGRLbU).mkv
s02/s02e25 Die Feuerpatrouille (YT 4dlXEbKTnKA).mp4
s02/s02e26 Der letzte Märchenwald (YT vDFuRMVhqKA).mp4
s02/s02e27 Chinas grüne Mauer (YT hPQpzybAEIU).mp4
s02/s02e28 Die Waldfabrik (YT i4IRpDalTSM).mp4
s02/s02e29 Himalaja Tödliche Höhe (YT c1KAS1kahk8).mp4
s02/s02e30 Apnoe-Taucher Im Tiefenrausch (YT j00DR-wJURo).mp4
s02/s02e30 Apnoe-Taucher Im Tiefenrausch (YT jCzsdDS3yRI).mp4
s02/s02e31 Radrennen Ewiger Endspurt (YT gqUU0m2KVqg).mp4
s02/s02e31 Radrennen Ewiger Endspurt (YT liSvczCI4aE).mp4
s02/s02e32 Sadhus Heilige Aussteiger (YT xI5D3TCuoYM).mkv
s02/s02e32 Sadhus Heilige Aussteiger (YT yMRU2rYV9cY).mp4
s02/s02e33 Die Elefantenschule (YT l6ciOHdMwlI).mp4
s02/s02e33 Die Elefantenschule (YT NY6caIukEX8).mkv
s02/s02e34 Der Rentier-Treck (YT kw2Mk9Su7zg).mp4
s02/s02e35 Nicht ohne meinen Hund (YT UOgEuKov234).mp4
s02/s02e36 Kamele im Rennen (YT LgBk0kjjk0E).mp4
s03/s03e01 Timbuktu (YT u1QLrA-PNrs).mkv
s03/s03e02 Die Frucht, die aus der Dürre kam (YT L1bcEWTOHm4).mp4
s03/s03e02 Die Frucht, die aus der Dürre kam (YT YIkyylhDf78).mp4
s03/s03e03 Baumeister der Wüste (YT r6iPQL1WZ_I).mp4
s03/s03e04 Wüste auf Bewährung (YT GA9d8JNQ0aY).mkv
s03/s03e05 Die Baustelle des Herrn (YT _1Ka_gTLjUw).mp4
s03/s03e06 Im Einsatz für den Nebelwald (YT gcOIjyneLdc).mp4
s03/s03e07 Hollywood auf dem Trockenen (YT 1Xs3akVZkZA).mp4
s03/s03e08 Die Adern von Berlin (YT PQJMws5-r_Y).mp4
s03/s03e08 Die Adern von Berlin (YT rh-tBQxi6Ro).mp4
s03/s03e09 Operation Alpentunnel (YT 9DqxNEBmpd8).mp4
s03/s03e09 Operation Alpentunnel (YT ZbGyoSRZNNA).mp4
s03/s03e10 Brücke in den Orient (YT n3SiL7t9T_s).mkv
s03/s03e10 Brücke in den Orient (YT X_u4jC40L_Q).mp4
s03/s03e11 Die letzten Nixen (YT a_MPCOQDmZE).mp4
s03/s03e12 Die Fischer von Rio Negro (YT WU516e1cZ2E).mp4
s03/s03e13 Anatomie einer Lawine (YT q9NdtLN4tHo).mp4
s03/s03e14 Die Erben Gandhis (YT qoO1ZxQk_iQ).mp4
s03/s03e14 Die Erbin Gandhis (YT qUfiXyZwcbw).mp4
s03/s03e15 Die Spur der Wüstenkrokodile (YT MFuattuR9DA).mp4
s03/s03e16 Invasion der Biber (YT 1lZYASab-T4).mp4
s03/s03e17 Kumbh Mela Das größte Fest der Welt (YT GygKg1HaK3U).mp4
s03/s03e18 Buzkashi Spiel der Steppenreiter (YT 6PKOPZ6vHfw).mp4
s03/s03e19 Wasserstoff im Tank (YT H-U9h4gjRpQ).mp4
s03/s03e19 Wasserstoff im Tank (YT U2ZGceieMCI).mkv
s03/s03e20 Stau am Himmel (YT dvHVBW4rOLY).mp4
s03/s03e21 Das Waisenhaus der Affen (YT bnV-Ze-vAZA).mp4
s03/s03e22 Die Bisonwächter (YT 1Bf6xUJ2jJ0).mp4
s03/s03e23 Die Farm der Schmetterlinge (YT bxBVKiUHOpE).mp4
s03/s03e24 Fährtensucher online (YT OWZJehCh4hk).mp4
s03/s03e25 Nepals verkaufte Töchter (YT zvAm_rmvynU).mkv
s03/s03e26 Die Stadt der Diamanten (YT 5G9nvOInLfA).mp4
s03/s03e27 Gaucho auf Lebenszeit (YT cJKLHLFDYXU).mp4
s03/s03e28 Der Großvater der Massai (YT oHFU1aOHGr0).mp4
s04/s04e01 Cunahá Tod im Regenwald (YT yzGLrkcry6c).mp4
s04/s04e02 Die Verwandtschaft der Wale (YT h5_HKyfGWqk).mp4
s04/s04e04 Im Schatten des Vulkans (YT VNj_YNRPecU).mkv
s04/s04e04 Party für eine Leiche (YT rw8zynFSFJo).mp4
s04/s04e04 Party für eine Leiche (YT VT0H2Jc0TQA).mkv
s04/s04e05 Filmstars im Pelz (YT gMcu-RgppR8).mp4
s04/s04e06 Hongkongs fliegende Küchen (YT tsr8CmfJ4cY).mp4
s04/s04e06 Hongkongs fliegende Küchen (YT tuvJUdvYD_A).mp4
s04/s04e07 Die Herren der Adler (YT HrEYNIQ3dUo).mp4
s04/s04e08 Safran, das teuerste Gewürz der Welt Ein blühendes Geschäft (YT a-LwN0C_I3U).mp4
s04/s04e09 Der Dreh mit den Havannas (YT kGDRh9FmLw4).mp4
s04/s04e10 Ein göttlicher Zug (YT UA8kICaAY_Q).mp4
s04/s04e11 Sinfonie der Straße (YT N-uzrMPGm3w).mkv
s04/s04e11 Sinfonie der Straße (YT XqG2GkP4BqI).mp4
s04/s04e12 Ticket in ein neues Leben (YT pi9fUEg6QJs).mp4
s04/s04e13 Die Bernsteintaucher (YT fGA6Fgc5tgQ).mp4
s04/s04e14 Mumien im Ausverkauf (YT T_VG6xORqgI).mp4
s04/s04e15 Die Minensucher von Kabul (YT 3wLFTh60fW8).mp4
s04/s04e17 Die Legende von den Killerbienen (YT rw9kCLRBqS4).mp4
s04/s04e18 Die Schule der Inuit (YT DvR4hXuzv1M).mp4
s04/s04e19 Peones Verkannte Helden (YT MXtyKNBctjU).mp4
s04/s04e21 Im Wald der Vampire (YT e1ufsFFCyzQ).mp4
s04/s04e22 Nashörner unter dem Hammer (YT NcnIjv7NEEg).mp4
s04/s04e23 Warten auf den Monsun (YT dei00bjPwvA).mp4
s04/s04e24 Palma Sola Stadt der Mörder (YT UwCJCZPcEL0).mp4
s04/s04e25 Bilder hören Die Blinden Kinder von Tibet (YT LTq7SwlTjaU).mp4
s04/s04e26 Der Blechmusik Oscar (YT mw6CLMWS17k).mp4
s04/s04e26 Der Blechmusik Oskar (YT OZGiwkf-WqI).mkv
s04/s04e27 Die Riesenflöße vom Jenissej – Ein Floßschiffer auf seiner Fahrt zum Polarmeer (YT 85nISbMK9ng).mkv
s04/s04e28 Heiratsmarkt in Marokko (YT 5mwI8g-fagQ).mp4
s04/s04e29 Die Türkischen Hochzeitsmacher (YT Nhy3yuYYp5s).mkv
s04/s04e30 Die Frachtensegler von Madagaskar (YT MOxGnaDNqe4).mp4
s04/s04e31 Die Abalone-Wilderer – Der Kampf um den Erhalt einer Seeschneckenart (YT kF1VEBBmF0A).mp4
s05/s05e01 Die Mörderinnen von Targsor – Das einzige Frauengefängnis in Rumänien (YT KYbUkoxaOyo).mkv
s05/s05e02 Das Metall aus dem Vulkan (YT RGqCVo2c3pQ).mkv
s05/s05e03 Die Söldner der Perlen (YT QsU9K1ZoEj8).mp4
s05/s05e04 Hongkongs Bambusakrobaten (YT BSIqpsZHcSw).mkv
s05/s05e05 Mission Nordkorea (YT PcX598GUNXw).mp4
s05/s05e06 Radios gegen Kalaschnikows (YT fsFFXBhSG6Q).mp4
s05/s05e07 Die Hightech Oase (YT sESu-VYdVFQ).mp4
s05/s05e07 Die Hightech-Oase – Auf der größten Milchfarm der Welt (YT 8gLLh2teor4).mkv
s05/s05e08 Videofabrik Nigeria (YT Tej9cR-hQ7o).mp4
s05/s05e09 Beuteltiere an der Börse (YT JTFfHASu6EI).mp4
s05/s05e10 Hongkong Pferde und Millionen (YT 3qb2dXghgjg).mp4
s05/s05e11 Wo der wilde Kaffee wächst (YT vqk-t5ZxJTg).mp4
s05/s05e12 Die Rückkehr der Meeresschildkröten (YT JHO9mBw2PYc).mp4
s05/s05e13 Samoa-Queens (YT 2jz1Lozi4dU).mkv
s05/s05e14 Einsatz für den Amur-Tiger (YT xdyhywULKUU).mp4
s05/s05e15 Die Seelensammler von Bangkok (YT kqy7qmiDe64).mp4
s05/s05e15 Die Seelensammler von Bangkok (YT ra8dlxRJWkc).mp4
s05/s05e16 Der Vogelhändler von Guangzhou (YT 3mrXlaxKolU).mp4
s06/10 Das Mysterium der sibirischen Mumie (360° - GEO Reportage) [DXk26Rs6ev8].mp4
s06/16 Der Polarflieger (360° - GEO Reportage) [JudMONhb6p0].mp4
s06/17 Dagestan – Land über den Wolken (360° - GEO Reportage) [E0QU7u1xbFM].mp4
s06/s06e01 Goldrausch in Sibirien (YT orPQ74toO10).mkv
s07/09 Das Postschiff zum Ende der Welt (360° - GEO Reportage) [hnuma6p1K08].mp4
s07/12 Die Eisenbahn vom Baikal zum Amur (360° - GEO Reportage) [GTkxMy9yVZM].mp4
s07/s07e12 Die Eisenbahn vom Baikal zum Amur (YT GTkxMy9yVZM).mkv
s07/s07e15 Das schwimmende Krankenhaus vom Amazonas (YT 0Xz-nWoBhUQ).mp4
s08/13 Auf den Dächern von Kairo (360° - GEO Reportage) [6rS22dz6_7o].mp4
s09/08 Bangkoks krabbelnde Delikatessen (360° - GEO Reportage) [Cxe2KMNhjG0].mp4
s10/18 Das Geheimnis der Schweizer Uhren (360° - GEO Reportage) [WhhdUVCFga0].mp4
s11/01 Arktis - Die Route der Atomeisbrecher (360° - GEO Reportage) [4VEpfXzy214].mp4
s11/19 Die Holzfäller von British Columbia (360° - GEO Reportage) [MpF684mvA5A].mp4
s11/s11e01 Arktis Die Route der Atomeisbrecher (YT 4VEpfXzy214).mp4
s12/12 Bishnoi, Tierliebe bis in den Tod (360° - GEO Reportage) [tcNmq-quVPA].mp4
s12/15 Baikalsee - ein Wintermärchen (360° - GEO Reportage) [Q32TkfdHpnI].mp4
s12/19 Anatolien, das Land wo die Aprikosen blühen (360° - GEO Reportage) [6UNZBLK5xHc].mp4
s12/s12e14 Taipan die gefährlichste Schlange der Welt (YT ItZXECu1GPQ).mp4
s13/02 Der Affenflüsterer und sein Traum (360° - GEO Reportage) [tsXjqdQkSio].mp4
s13/07 Das Perlenimperium von Palawan (360° - GEO Reportage) [7KKgclOqxAU].mp4
s13/12 Armenien, die Früchte aus dem Paradies (360° - GEO Reportage) [25Vub7M_rLc].mp4
s13/14 Die Halligen mitten im Winter, mitten im Wasser (360° - GEO Reportage) [qZMtcyipMQc].mp4
s13/s13e01 Fremdenlegion, die Hölle im Regenwald (YT p3uxoko70Cc).mp4
s14/03 China, im Reich der Musuo-Frauen (360° - GEO Reportage) [GhMq7fkeUKI].mp4
s14/19 Bolivien, Lebensader Todesstraße (360° - GEO Reportage) [JhplvCSCDkQ].mp4
s15/04 Atacamawüste - Leben ohne Wasser (360° - GEO Reportage) [OJJze1tQhz0].mp4
s15/25 Der gute Mensch von Karachi (360° - GEO Reportage) [pk9M0hHj6e4].mp4
s15/s15e14 Die Polarbahn (YT VJ6JS8MWo9Y).mp4
s16/08 Bangkoks Schatztaucher (360° - GEO Reportage) [RKq3lqts3lg].mp4
s16/15 Bolivien - Kleine Käfer, großes Geld! (360° - GEO Reportage) [jOGkfs9xLlk].mp4
s16/23 Die Eisbergjäger von Neufundland (360° - GEO Reportage) [Jylj5OMHrWk].mp4
s16/s16e01 Vietnam, Kobra auf dem Teller (YT k5mRGmiLhBA).mp4
s16/s16e03 Kambodscha, Ratte süß-sauer (YT Fadu9DpauSQ).mp4
s17/22 David und die Komodowarane (360° - GEO Reportage) [6uFzOGhS8UI].mp4
s17/23 China, Braut ohne Bräutigam (360° - GEO Reportage) [e9nzSo2Tqr8].mp4
s18/08 Die Bärenhunde von Nevada (360° - GEO Reportage) [wf024fhwmvw].mp4
s18/11 China - Die Eisfischer vom Chagan-See (360° - GEO Reportage) [vPLT2RVso_Y].mp4
s19/s19e24 Sibirien, die Polarstraße ins Polarmeer (YT S7VcirrE2xc).mp4
s22/02 Costa Rica, das größte Hundeheim der Welt (360° - GEO Reportage) [5N1mFKBBFLg].mp4
s22/15 Der letzte Rheinfischer (360° - GEO Reportage) [1JPQTQtsjyA].mp4
s23/16 Der Wüstenzug, die Lebensader Mauretaniens (360° - GEO Reportage) [k9jFka2IecU].mp4
s24/s24e16 Nopal, der Alleskönner aus Mexiko (YT MkXx_8rac_M).mp4
s24/s24e17 Mit Tempo und Leidenschaft Argentiniens Polo-Spielerinnen (YT Y-eQibAkbmo).mp4
s24/s24e18 Kourou Palmen, Raketen, Gefängnisinseln (YT LckZ2_Lw88E).mp4
s24/s24e19 Las Fallas Valencias feurige Fiesta (YT ug2XFpN43CU).mp4
s24/s24e21 Indien Kampf den Scharlatanen (YT -Clpkb3JdkI).mp4
s24/s24e22 Ahornsirup Kanadas süßer Schatz (YT HlFRnPw6Y04).mp4
"""


json_file = open("episodes.json", "r")


class Episode(typing.TypedDict):
    id: str
    season: int
    episode: int
    no: int
    title: str
    air_data: str
    duration: int
    thetvdb_episode_no: int


episodes: list[Episode] = json.load(json_file)


src_titles: list[str] = []
for episode in episodes:
    # print(episode['title'])
    src_titles.append(episode["title"])


def extract_title_from_new(rel_path: str) -> str:
    """
    _new/Sark, die Kanalinsel der Queen (360° - GEO Reportage) [ybpV9JWD6qs].mp4

    -> Sark, die Kanalinsel der Queen
    """
    rel_path = rel_path.replace("_new/", "")
    rel_path = rel_path.replace("_new/", "")
    rel_path = re.sub(r" \(.*", "", rel_path)
    return rel_path


def get_episode_by_title(title: str | None) -> Episode | None:
    if not title:
        return
    match: list[str] = difflib.get_close_matches(title, src_titles, n=1)
    if len(match) > 0:
        src_i: int = src_titles.index(match[0])
        return episodes[src_i]


dest_titles: list[str | None] = []
dest_files: list[str] = []
for rel_path in files.splitlines():
    dest_files.append(rel_path)
    if rel_path.startswith("_new"):
        title = extract_title_from_new(rel_path)
        print(title)
        dest_titles.append(title)
    else:
        dest_titles.append(None)

dest_i = 0
for title in dest_titles:
    episode: Episode | None = get_episode_by_title(title)
    if episode:
        src = pathlib.Path(dest_files[dest_i])
        print(episode["title"])
        print(src)

        season: str = str(episode['season']).zfill(2)
        dest: str = f"s{season}/{episode['id'].lower()} {src.name}"

        dest = re.sub(r" +\(.*\) +", " ", dest)
        dest = re.sub(r"\[(.*)\]+", r"(YT \1)", dest)
        print(dest)
        # print(episode)
        # src.rename(dest)
        print()
    dest_i += 1
