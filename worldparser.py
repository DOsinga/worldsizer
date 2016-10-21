#!/usr/bin/env python
import math
import pyproj
import shapefile
import pprint
import json
from collections import defaultdict, Counter

CC_CODES = {
  'Taiwan': 'tw',
  'Western Sahara': 'eh',
}

EXTRA_BRIDGES = [
  ('es', 'ma'),
  ('tr', 'gr'),
  ('se', 'dk'),
  ('ry', 'so'),
  ('nz', 'au'),
]

def calc_area(pts):
  n = len(pts) # of corners
  area = 0.0
  for i in range(n):
      j = (i + 1) % n
      area += pts[i][0] * pts[j][1]
      area -= pts[j][0] * pts[i][1]
  return abs(area) / 2.0


MAGIC_MOLL_NUMBER = 9020047.848073646
SRC_PROJ = pyproj.Proj(proj='longlat', ellps='WGS84', datum='WGS84')
DST_PROJ = pyproj.Proj(proj='moll', lon_0=0, x_0=0, y_0=0, ellps='WGS84', datum='WGS84', units='m')

def project_point(pt):
  x, y = pyproj.transform(SRC_PROJ, DST_PROJ, pt[0], pt[1])
  return (x / 2 + MAGIC_MOLL_NUMBER) / (MAGIC_MOLL_NUMBER * 2), (MAGIC_MOLL_NUMBER - y) / (MAGIC_MOLL_NUMBER * 2)


def extract_shapes(shape):
  points = [project_point(pt) for pt in shape.points]
  if shape.parts == [0]:
    res = [list(points)]
  else:
    parts_idx = list(shape.parts) + [len(points)]
    res = [points[parts_idx[i]: parts_idx[i + 1]] for i in range(len(shape.parts))]
  return res


def index_shape(sh, all_points, all_points_index):
  res = []
  sum_x = 0
  sum_y = 0
  prev_key = None
  for pt in sh:
    sum_x += pt[0]
    sum_y += pt[1]
    key = '%2.5f-%2.5f' % pt
    if key == prev_key:
      continue
    prev_key = key
    if not key in all_points_index:
      all_points_index[key] = len(all_points)
      all_points.append(pt)
    res.append(all_points_index[key])
  # if the first and last are the same, eliminate, the system will close the loop
  if res[0] == res[-1]:
    res = res[:-1]
  return {'x': sum_x / len(sh),
          'y': sum_y / len(sh),
          'area': calc_area(sh),
          'bridges': [],
          'pts': res}

def distance_squared(pt1, pt2):
  dx = pt1[0] - pt2[0]
  dy = pt1[1] - pt2[1]
  return dx * dx * 4 + dy * dy

def main():
  r = shapefile.Reader('data/ne_110m_admin_0_countries')
  labels = [x[0] for x in r.fields]
  all_points = []
  all_points_index = {}
  indexed_shapes = [[index_shape(sh, all_points, all_points_index) for sh in extract_shapes(shape)]
                    for shape in r.shapes()]
  sizes = [sum(sh['area'] for sh in shapes) for shapes in indexed_shapes]

  counts = Counter()
  for shapes in indexed_shapes:
    for shape in shapes:
      for pt in shape['pts']:
        counts[pt] += 1
  dupes = {k for k, v in counts.items() if v > 1}
  for shapes in indexed_shapes:
    for shape in shapes:
      shape['island'] = not any(pt in dupes for pt in shape['pts'])

  total_size = sum(sizes)
  recs = [dict(zip(labels, x)) for x in r.records()]
  for rec in recs:
    cc = rec['un_a3']
    if not cc or cc == '-99':
      cc = rec['fips_10']
    if not cc or cc == '-99':
      cc = CC_CODES.get(rec['name'])
    else:
      cc = cc.lower()
    rec['cc'] = cc

  point_to_shape = {}
  for idx, shapes in enumerate(indexed_shapes):
    cc = recs[idx]['cc']
    for shape in shapes:
      for pt in shape['pts']:
        point_to_shape[pt] = (cc, shape)

  # Find for islands nearby anchors.
  # This doesn't make too much sense since we're in a non distance preserving
  # projection. We should probably *also* save the lat/lng for each shape
  # and then use the spherical distance here. Oh well.
  geo_index = defaultdict(list)
  for idx, pt in enumerate(all_points):
    geo_index[int(500 * pt[1]) * 500 + int(500 * pt[0])].append((idx, pt, point_to_shape[idx]))

  for idx, shapes in enumerate(indexed_shapes):
    cc = recs[idx]['cc']
    for shape in shapes:
      if shape['island'] or cc == 'ie':
        min_x = min(all_points[p][0] for p in shape['pts'])
        max_x = max(all_points[p][0] for p in shape['pts'])
        min_y = min(all_points[p][1] for p in shape['pts'])
        max_y = max(all_points[p][1] for p in shape['pts'])
        min_x = max(0, int((min_x - 4 / 500) * 500))
        max_x = min(500, int((max_x + 4 / 500) * 500))
        min_y = max(0, int((min_y - 6 / 500) * 500))
        max_y = min(500, int((max_y + 6 / 500) * 500))
        own_pts = set(shape['pts'])

        own_cnt = 0
        near = []
        for x in range(min_x, max_x):
          for y in range(min_y, max_y):
            for pt in geo_index[x + y * 500]:
              if not pt[0] in own_pts:
                near.append(pt)
              else:
                own_cnt += 1

        shape_center = (shape['x'], shape['y'])
        bridges = []
        for idx, pt, (pt_cc, other_shape) in sorted(near, key=lambda other:distance_squared(other[1], shape_center)):
          if other_shape['island'] and other_shape['area'] < shape['area']:
            # only bridge to larger land masses to avoid conflicts
            continue
          distance = math.sqrt(distance_squared(pt, shape_center))
          for _, bridge_pt, _ in bridges:
            if math.sqrt(distance_squared(bridge_pt, pt)) < distance:
              break
          else:
            bridges.append((idx, pt, pt_cc))
        shape['bridges'] = [(idx, pt[0] - shape['x'], pt[1] - shape['y'], pt_cc) for idx, pt, pt_cc in bridges]

  countries = [{'name': str(rec['name']),
                'cc': rec['cc'],
                'shapes': shapes,
                'region': str(rec['region_un']),
                'continent': str(rec['continent']),
                'weight': size / total_size}
               for rec, shapes, size in zip(recs, indexed_shapes, sizes)
               if rec['cc']]

  countries_by_cc = {country['cc']: country for country in countries}
  for cc1, cc2 in EXTRA_BRIDGES:
    country1 = countries_by_cc[cc1]
    country2 = countries_by_cc[cc2]
    shape1 = max(country1['shapes'], key=lambda shape:shape['area'])
    shape2 = max(country2['shapes'], key=lambda shape:shape['area'])
    if shape1['area'] < shape2['area']:
      shape1, shape2 = shape2, shape1
      country1, country2 = country2, country1

    shape1_ct = (shape1['x'], shape1['y'])
    pt_idx = min(shape2['pts'], key=lambda pti:distance_squared(shape1_ct, all_points[pti]))
    x, y = all_points[pt_idx]
    shape1['bridges'].append((pt_idx, x - shape1['x'], y - shape1['y'], country1['cc']))


  with open('data/countries.py', 'w') as fout:
    fout.write('COUNTRIES=' + pprint.pformat(countries) + '\n' +
               'POINT_INDEX=' + pprint.pformat(all_points) + '\n'
    )
  with open('data/countries.js', 'w') as fout:
    fout.write('COUNTRIES=' + json.dumps(countries, indent=2) + ';\n' +
               'POINT_INDEX=' + json.dumps(all_points, indent=2) + ';\n'
    )

if __name__ == '__main__':
  main()





