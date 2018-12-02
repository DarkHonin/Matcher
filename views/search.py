from flask.views import MethodView
from flask import Flask, render_template, request, jsonify, redirect, url_for
from systems.properties import check_captcha, RequestValidator
from systems.exceptions import SystemException
from systems.users import User, UserInfo, requires_Users
from systems.tokens import redeemToken
from systems.telemetry import Telemetry
import datetime
from dateutil.relativedelta import relativedelta
from systems.search import SearchEngine

class Search(MethodView):

	def recurMerge(self, dicta, dictb):
		ret = {}
		for (i, v) in dicta.items():
			if i not in ret:
				ret[i] = v
		for (i, v) in dictb.items():
			if i not in ret:
				ret[i] = v
			else:
				ret[i] = self.recurMerge(ret[i], v)
		return ret

	def get(self):
		db_pass = {}
		expects = ["name", "min_age", "max_age", "sort", "dir", "age_gap", "distance"]
		params = {}
		for i in expects:
			params[i] = request.args.get(i, "")
		for i, f in {"name" : self.filerNames, "min_age" : self.minAge,"max_age" : self.maxAge}.items():
			query = request.args.get(i, False)
			if query:
				params[i] = query
				db_pass = self.recurMerge(db_pass, f(query))
		data = UserInfo.get(db_pass, {"fname" : 1, "lname" : 1, "uname" : 1, "interest" : 1, "gender" : 1, "images" : 1, "_dob" : 1, "location" : 1})
		if isinstance(data, list):
			result = [ f.toDisplaySet() for f in data]
		else:
			if data:
				result = [data.toDisplaySet()]
			else:
				result = {}
		sort = request.args.get("sort", False)
		direct = request.args.get("dir", "0") == "1"
		result = self.applyAdvancedSort(result, ageGap=request.args.get("age_gap", False), location=request.args.get("distance", False))
		if sort:
			result.sort(key=lambda x : x[sort], reverse=direct)
		return render_template("pages/user/search.html", users=result, **params)

	def applyAdvancedSort(self, data, location, ageGap):
		pool = {}
		try:
			if location and int(location) > 0:
				pool["location"] = int(location)
			if ageGap and int(ageGap) > 0:
				pool["age"] = int(ageGap)
		except ValueError:
			raise SystemException("Invalid number supplied to range search", SystemException.FIELD_ERROR)
		search = SearchEngine(data, 15, pool, {"location" : 1, "age" : 1})
		return search.search()

	def filerNames(self, name):
		return {"$or" : [ 
				{"uname" : {"$regex" : (".*%s.*" % name)}},
			{"lname" : {"$regex" : (".*%s.*" % name)}},
			{"fname" : {"$regex" : (".*%s.*" % name)}}
			]}

	def minAge(self, date):
		time = datetime.datetime.now() - relativedelta(years=int(date))
		return {"dob" : {'$lt' : time}}

	def maxAge(self, date):
		end = datetime.datetime.now() - relativedelta(years=int(date))
		return {"dob" : {"$gte" : end}}

	def post(self):
		data = request.get_json()
		for i in data.keys():
			for i, k in {"Names" : self.forUsername, "ageGap" : self.forAgeGap}.items():
				if i in data:
					return k(data[i])
		raise SystemException("Invalid search query", SystemException.FIELD_ERROR)

	@classmethod
	def bind(cls, app : Flask):
		app.add_url_rule("/search", view_func=cls.as_view("search"))
