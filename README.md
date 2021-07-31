# transfermarkt-data-explore

## Dependencies

Developed with Python 3.8.3, see [requirements.txt](requirements.txt)for the list of packages.

## Description

This script extract data from transfermarkt,
in order to analyse the relationship between country of birth and national team

The transformed data is output to the [results\nationality_players.csv](results\nationality_players.csv) file.

The csv can be explored using Excel (with Pivot tables) or Jupyter Notebooks.

## Top Countries of births

```python
df.groupby('country_birth')\
    .size()\
    .sort_values(ascending=False)\
    .head(10)
```

```
France                    188
England                   142
Netherlands                84
UdSSR                      84
United States              70
Spain                      62
Germany                    60
Portugal                   58
Yugoslavia (Republic)      51
```

### France

```python
df[df.country_birth=='France']\
    .groupby('country_fifa')\
    .size()\
    .sort_values(ascending=False)\
    .head(15)
```

```
Comoros                     27
France                      23
Algeria                     16
Gabon                       10
Tunisia                     10
Benin                        9
Madagascar                   9
Mauritania                   8
Cote d'Ivoire                8
Senegal                      7
Congo                        7
Haiti                        6
Cameroon                     6
Central African Republic     6
DR Congo                     5
```

The map of the former French colonies almost appear straight for this query.
Most of the players are second-generation immigrants who play for their parents'
country to get more chance to join international competitions such as the Africa Cup of Nations or the World Cup.

Fun fact: there are more players born in France in the Comorian team than in the French team!

### England

```python
df[df.country_birth=='England']\
    .groupby('country_fifa')\
    .size()\
    .sort_values(ascending=False)\
    .head(10)
```

```
England                25
Montserrat             16
Grenada                11
Wales                   9
Jamaica                 9
Northern Ireland        7
Guyana                  7
Antigua and Barbuda     5
St. Kitts & Nevis       5
Gibraltar               5
Ireland                 5
Pakistan                4
Scotland                3
Barbados                3
Sierra Leone            2
```

A similar pattern emerges for England, although more specific.
The players are mostly from other UK nations and dual citizens from Caribbean islands.
Unlike France, there aren't many former African colonies (Nigeria, Ghana, Kenya, Sudan, ...).

### Netherlands

```python
df[df.country_birth=='Netherlands']\
    .groupby('country_fifa')\
    .size()\
    .sort_values(ascending=False)\
    .head(10)
```

```
Netherlands    24
Curacao        19
Suriname       11
Aruba           7
Afghanistan     3
Somalia         3
Morocco         3
Barbados        2
Cape Verde      2
Turkey          2
```

The list reveals shows connection to Dutch overseas territories (Curacao, Aruba),
former colony (Suriname) and more recent immigrant's countries (Afghanistan, Somalia,
Morocco, Cape Verde, Turkey).