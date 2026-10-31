import test_ac2

class NutritionTest(test_ac2.MealsTest):
    def test_complete_ac1_ac2_flow(self):
        tokens=[]
        for email in ['resumo@example.com','outra@example.com']:
            self.request('POST','/auth/register',{'name':'Teste','email':email,'password':'teste123'},expected=201)
            tokens.append(self.request('POST','/auth/login',{'email':email,'password':'teste123'})['access_token'])
        a,b=tokens
        path='/dashboard?date=2026-10-30'
        self.request('GET',path,expected=403)
        self.assertIsNone(self.request('GET','/goals',token=a))
        self.assertEqual(self.request('GET',path,token=a)['totals']['calories'],0)
        goal={'calories':200,'protein':20,'carbs':30,'fat':10}
        self.request('PUT','/goals',goal,a)
        for key in goal:
            for value in [0,-1,999999,float('inf')]:
                self.request('PUT','/goals',{**goal,key:value},a,422)
        food=self.request('POST','/foods',{'name':'Exemplo','calories':200,'protein':10,'carbs':20,'fat':5},a,201)
        payload={'date':'2026-10-30','meal_type':'lunch','items':[{'food_id':food['id'],'quantity_g':150}]}
        meal=self.request('POST','/meals',payload,a,201)
        result=self.request('GET',path,token=a)
        self.assertEqual(result['totals'],{'calories':300,'protein':15,'carbs':30,'fat':7.5})
        self.assertEqual(result['progress']['calories'],150)
        self.assertEqual(result['meal_count'],1)
        self.assertIsNone(self.request('GET','/goals',token=b))
        self.assertEqual(self.request('GET',path,token=b)['totals']['calories'],0)
        self.assertEqual(self.request('GET','/dashboard?date=2026-10-29',token=a)['meal_count'],0)
        self.request('GET','/dashboard?date=bad',token=a,expected=422)
        self.process.terminate();self.process.wait(timeout=10);self.__class__.start_server()
        self.assertEqual(self.request('GET','/goals',token=a),goal)
        self.assertEqual(self.request('GET',path,token=a)['totals']['calories'],300)
        payload['items'][0]['quantity_g']=50
        self.request('PUT',f'/meals/{meal["id"]}',payload,a)
        self.assertEqual(self.request('GET',path,token=a)['totals']['calories'],100)
        self.request('PUT','/goals',{**goal,'calories':400},a)
        self.assertEqual(self.request('GET',path,token=a)['progress']['calories'],25)
        self.request('DELETE',f'/meals/{meal["id"]}',token=a,expected=204)
        self.assertEqual(self.request('GET',path,token=a)['totals']['calories'],0)
