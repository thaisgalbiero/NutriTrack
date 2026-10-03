"""Integração HTTP com SQLite temporário; execute python -m unittest discover -s tests -v."""
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time
import unittest
from urllib.request import Request, urlopen
from urllib.error import HTTPError


class MealsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        with socket.socket() as sock:
            sock.bind(('127.0.0.1', 0))
            cls.port = sock.getsockname()[1]
        cls.url = f'http://127.0.0.1:{cls.port}'
        cls.env = {**os.environ, 'DATABASE_URL': f'sqlite:///{cls.temp.name}/test.db'}
        cls.start_server()

    @classmethod
    def start_server(cls):
        cls.process = subprocess.Popen([sys.executable, '-m', 'uvicorn', 'app.main:app', '--port', str(cls.port)],
            cwd=Path(__file__).resolve().parents[1], env=cls.env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(100):
            try:
                with urlopen(cls.url, timeout=1):
                    return
            except OSError:
                time.sleep(.05)
        raise RuntimeError('API não iniciou')

    @classmethod
    def tearDownClass(cls):
        cls.process.terminate()
        cls.process.wait(timeout=10)
        cls.temp.cleanup()

    def request(self, method, path, body=None, token=None, expected=200):
        headers = {'Content-Type': 'application/json'}
        if token:
            headers['Authorization'] = f'Bearer {token}'
        req = Request(self.url + path, data=json.dumps(body).encode() if body is not None else None,
                      headers=headers, method=method)
        try:
            response = urlopen(req)
        except HTTPError as error:
            response = error
        with response:
            raw = response.read()
            self.assertEqual(response.status, expected, raw.decode())
            return json.loads(raw) if raw else None

    def test_complete_ac1_ac2_flow(self):
        tokens = []
        for email in ['ana@example.com', 'bia@example.com']:
            self.request('POST', '/auth/register', {'name': 'Teste', 'email': email, 'password': 'teste123'}, expected=201)
            tokens.append(self.request('POST', '/auth/login', {'email': email, 'password': 'teste123'})['access_token'])
        a, b = tokens
        food = self.request('POST', '/foods', {'name': 'Banana', 'calories':89, 'protein':1.1, 'carbs':22.8, 'fat':.3}, a, 201)
        self.assertEqual(len(self.request('GET', '/foods', token=a)), 1)
        self.request('GET', '/meals?date=2026-10-02', expected=403)
        self.request('GET', '/meals?date=2026-10-02', token='invalid', expected=401)
        payload = {'date':'2026-10-02', 'meal_type':'breakfast', 'meal_time':'08:30', 'notes':'Antes da aula', 'items':[{'food_id':food['id'], 'quantity_g':120}]}
        meal = self.request('POST', '/meals', payload, a, 201)
        mid = meal['id']
        self.assertEqual(meal['meal_time'], '08:30')
        self.assertEqual(meal['items'][0]['food']['name'], 'Banana')
        self.assertEqual(len(self.request('GET', '/meals?date=2026-10-02', token=a)), 1)
        self.assertEqual(self.request('GET', '/meals?date=2026-10-03', token=a), [])
        self.assertEqual(self.request('GET', '/meals?date=2026-10-02', token=b), [])
        self.request('PUT', f'/meals/{mid}', payload, b, 404)
        self.request('DELETE', f'/meals/{mid}', token=b, expected=404)
        for patch in [ {'meal_time':'24:00'}, {'meal_time':'12:60'}, {'meal_time':'8:00'}, {'meal_time':''}, {'items':[]}, {'meal_type':'invalid'}, {'date':'bad'}, {'notes':'x'*501},
                       {'items':[{'food_id':9999,'quantity_g':1}]},
                       {'items':[{'food_id':food['id'],'quantity_g':0}]},
                       {'items':[{'food_id':food['id'],'quantity_g':-2}]},
                       {'items':payload['items']*2} ]:
            self.request('POST', '/meals', {**payload,**patch}, a, 422)
        self.request('PUT', f'/meals/{mid}', {**payload,'items':[]}, a, 422)
        payload.update(date='2026-10-03',meal_type='lunch', meal_time='12:45', notes='Atualizada')
        payload['items'][0]['quantity_g'] = 150
        updated = self.request('PUT', f'/meals/{mid}', payload, a)
        self.assertEqual(updated['items'][0]['quantity_g'], 150)
        self.assertEqual(updated['meal_time'], '12:45')
        legacy_payload = {k:v for k,v in payload.items() if k != 'meal_time'}
        self.assertEqual(self.request('PUT', f'/meals/{mid}', legacy_payload, a)['meal_time'], '12:45')
        import sqlite3
        with sqlite3.connect(f'{self.temp.name}/test.db') as db:
            self.assertEqual(db.execute('SELECT horario, refeicao, alimento, quantidade_g FROM vw_refeicoes_detalhadas').fetchone(), ('12:45', 'Almoço', 'Banana', 150))
        self.assertEqual(self.request('GET', '/meals?date=2026-10-02', token=a), [])
        # Reiniciar a API comprova persistência no arquivo SQLite.
        self.process.terminate(); self.process.wait(timeout=10)
        self.__class__.start_server()
        self.assertEqual(self.request('GET', '/meals?date=2026-10-03', token=a)[0]['notes'], 'Atualizada')
        self.assertEqual(self.request('GET', '/meals?date=2026-10-03', token=a)[0]['meal_time'], '12:45')
        self.assertIsNone(self.request('PUT', f'/meals/{mid}', {**payload, 'meal_time':None}, a)['meal_time'])
        self.request('DELETE', f'/meals/{mid}', token=a, expected=204)
        self.assertEqual(self.request('GET', '/meals?date=2026-10-03', token=a), [])
        self.request('DELETE', f'/meals/{mid}', token=a, expected=404)
        for kind in ['breakfast','lunch','dinner','snack']:
            self.request('POST', '/meals', {**payload,'meal_type':kind}, a, 201)
        self.assertEqual(len(self.request('GET', '/meals?date=2026-10-03', token=a)), 4)
        import sqlite3
        with sqlite3.connect(f'{self.temp.name}/test.db') as db:
            self.assertEqual(db.execute('SELECT count(*) FROM meal_items').fetchone()[0], 4)


if __name__ == '__main__':
    unittest.main()
