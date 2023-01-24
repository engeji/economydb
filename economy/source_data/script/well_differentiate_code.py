import os
import datetime
import random
from pathlib import Path
import numpy as np
import re
import math
from os import path

#//////////////////////////////////////////////////#
_GROUP = 'all' # группа  Группа: all, ukpg_1, _1b_old, _1b_new, _1b_new_2, ukpg_2, _2b_old, _2b_new, _2b_new_2, _3b_old
_OBJECT = 'all' # 'all' # Объект: 'I', 'II' - Объекты; 1-17 пласты
_FILENAME = 'well_table_01_2022_DTPR.txt'
#//////////////////////////////////////////////////#

'''
Исходная информация
'''
PRECISION = 20 #количество знаков после запятой
START_DATE = '01.01.2021' #дата с которой необходимо выгружать показатели
MODEL = get_model_by_name ('Var3_red_2_DTPR_2022')
DATAPATH = os.path.dirname(os.path.abspath("__file__")) + r'/script_data/'
TIMESTEPS = get_all_timesteps()


class Welldataholder:
	
	list_of_poks = [
					'dry_gas', 
					'stab_cond', 
					'res_gas', 
					'gas_sep', 
					'nestab_cond', 
					'wbp', 
					'wbhp', 
					'wthp'
					]
	
	pok_dic = {i:pok for i,pok in enumerate(list_of_poks)}

	def __init__(self, wname, tstep, kwargs):
		
		self.wname = wname
		self.tstep = tstep
		
		for key, pok in kwargs.items():
			setattr(self,key, pok)

	@classmethod
	def output_header(cls, welldic):
		s = '\t'
		
		
		for item in welldic.keys():
			space = '\t'*(len(cls.pok_dic.keys()))
			s += f'{item}{space}'
		s += '\n\t'
		
		temp_s =  ''
		for item in cls.pok_dic.values():
			temp_s += f'{item}\t'
			
		s += temp_s * (len(welldic.keys())) + '\n'
		return s

	def output_data(self):
		s = ''#f'{self.tstep}\t'
		
		for item in self.pok_dic.values():
			val = getattr(self, item)
			s += f'{val:0.3f}\t'
		return s
	
class ObjectNotFoundError(Exception):
	'''
	Исключение - вызывается тогда, когда объект не найден в словаре объектов, 
	вложенного класса Objects клсса Groups
	'''
	def __init__(self, message):
		self.message = message
class m(type):
# метакласс для сабскрипта классов и вызова итератора словаря-контейнера экземляров
	def __getitem__(cls, key):
		return cls._dic[key]
	def __iter__(cls):
		return iter(cls._dic.values())	


class Groups(metaclass = m):
	'''
	класс хранит в себе сет скважин, принадлежащий к группе из макроса. 
	Исходные данные по накопленным 
	'''
	
	_dic = {}

	class Object:
	# Для каждой группы содержит в себе информацию по объекту, диапазоны соединений, исходную информации фактической точки отсчета
		_reg_list = []
		def __init__(self, name = None, start = None, end = None, t = None, water_density = None):
			self.name = name
			self.start = start
			self.end = end
			self.t = t
			self.res_gas = 1
			self.res_oil = 1
			self.plast_rate = 0
			self.plast_total = 0
			self.dry_rate = 0
			self.dry_total = 0 
			self.oil_total = 0
			self.oil_rate = 0
			self.gas_sep_rate = 0
			self.nestab_cond = 0
			self.water_density = water_density
			Groups.Object._reg_list.append(self)
			
		def get_wetness(self, _cbp):
			a = 4.67* math.exp(0.0735*self.t - 0.00027*self.t*self.t)
			b = 0.0418*math.exp(0.054*self.t - 0.0002*self.t*self.t)
			try:
				wetness = (a/_cbp + b)/(self.water_density/1000)
				
			except ZeroDivisionError:
				return 0
			return wetness
			
		@classmethod
		def get_wetness_func(cls, k):
			
			for obj in cls._reg_list:
				if obj.name == 'all':
					continue
				if obj.start <= k <=obj.end:
					return obj.get_wetness
					
	def __init__(self, name, object = 'all'):
		self.name = name
		
		try:
			'''
			tnav_obj - предопределенный объект навика, если группа нет в Groups тнава,
			то tnav_obj - None
			'''
			self.tnav_obj = get_group_by_name (name)
			self.well_set = self.group_by_well(name)
		except:
			self.tnav_obj = None
			self.well_set = set()
			
		'''
		Блок инициализации объектов разработки (имя объекта, к1, к2)
		'''
		self._objects = {}
		self._objects['all'] = self.Object('all')
		self._objects['I'] = self.Object('I', 1, 48, 71,998.4)
		self._objects['II'] = self.Object('II', 50, 298, 84, 998.3)
		self._objects[1] = self.Object('БУ_3 1', 1, 17, 71, 998.4)
		self._objects[2] = self.Object('БУ_4 1', 19, 30, 71, 998.4)
		self._objects[3] = self.Object('БУ_4 2-3', 32, 48, 71, 998.4)
		self._objects[4] = self.Object('БУ_6 1', 50, 61, 84, 998.3)
		self._objects[5] = self.Object('БУ_6 2', 63, 74, 84, 998.3)
		self._objects[6] = self.Object('БУ_6 3', 76, 97, 84, 998.3)
		self._objects[7] = self.Object('БУ_7', 99, 117, 84, 998.3)
		self._objects[8] = self.Object('БУ_8 0', 119, 126, 84, 998.3)
		self._objects[9] = self.Object('БУ_8 01', 128, 137, 84, 998.3)
		self._objects[10] = self.Object('БУ_8 02', 139, 146, 84, 998.3)
		self._objects[11] = self.Object('БУ_8 1', 148, 165, 84, 998.3)
		self._objects[12] = self.Object('БУ_8 2', 167, 182, 84, 998.3)
		self._objects[13] = self.Object('БУ_8 3', 184, 203, 84, 998.3)
		self._objects[14] = self.Object('БУ_9 0', 205, 228, 84, 998.3)
		self._objects[15] = self.Object('БУ_9 1', 258, 281, 84, 998.3)
		self._objects[16] = self.Object('БУ_9 1-1', 258, 281, 84, 998.3)
		self._objects[17] = self.Object('БУ_9 2', 283, 298, 84, 998.3)
		Groups._dic[self.name] = self
	

		
	def group_by_well(self, name):
	# функция возвращает сет скважин, принадлежаший данной группе
		well_list = self.tnav_obj.all_wells
		s = set()	
		
		'''
		Кусок кода возвращает сет скважин, которые есть в файле well_table.txt и присваивает их атрибуту класса, 
		этот сет скважин принадлежит конкретно к экземпляру класса.
		'''
		for well in well_list:
			try:
				s.add(Wells[well.name])
			except KeyError:
				continue
		return s

	@property
	def objects(self):
		return iter(self._objects.values())
		
	def __iter__(self):
		return iter(self.well_set)

	def __add__(self, other):
	# объединение двух групп, возвращает новый экземпляр класса
		g = Groups(self.name +'_' + other.name)
		g.tnav_obj = None
		g.well_set = set.union(self.well_set, other.well_set)
		for key in self._objects.keys():
			g._objects[key].res_gas = self._objects[key].res_gas + other._objects[key].res_gas
			g._objects[key].res_oil = self._objects[key].res_oil + other._objects[key].res_oil
			g._objects[key].plast_rate = self._objects[key].plast_rate + other._objects[key].plast_rate 
			g._objects[key].plast_total = self._objects[key].plast_total + other._objects[key].plast_total
			g._objects[key].dry_rate = self._objects[key].dry_rate + other._objects[key].dry_rate
			g._objects[key].dry_total = self._objects[key].dry_total + other._objects[key].dry_total
			g._objects[key].oil_total = self._objects[key].oil_total + other._objects[key].oil_total
			g._objects[key].oil_rate = self._objects[key].oil_rate + other._objects[key].oil_rate
			g._objects[key].gas_sep_rate = self._objects[key].gas_sep_rate + other._objects[key].gas_sep_rate
			g._objects[key].nestab_cond = self._objects[key].nestab_cond + other._objects[key].nestab_cond 
		return g
		
	def __getitem__(self, object_name):
	# возвращает сет скважин, принадлежащий к объекту object
		return self._objects[object_name]
		
	@classmethod
	def get_groups(cls):	
		'''
		функция парсит текстовики в папке //groups для инициализации фактической точки 
		отсчета показателей
		'''
		data = DATAPATH + 'groups'
		arr = os.listdir(data)
		for filename in arr:
			copy = filename
			splited_filename = copy.replace('.', '_').split('_')
			file = open(f'{data}\\{filename}')
			lines = file.readlines()
			file.close()
			try:
				group_obj = cls._dic[lines[0].split()[2]]
				#print(lines[0].split()[2])
			except KeyError:
				#print(f'Group {lines[0].split()[2]} is not initialized')
				continue
			obj = group_obj._objects[lines[1].split()[2]]
			#print(obj.plast_rate)
			for i in range(2, len(lines)):
				attr_name = lines[i].split()[0]
				val = lines[i].split()[2]
				obj.__setattr__(attr_name, float(val))


class Graphs():
	'''
	класс-контейнер, хранит показатели для экспорта, 
	как в виде графиков, так и в виде таблицы
	'''
	_graphs = []
	def __init__(self, name, units = ''):
		self.name = name
		self.units = units
		self.graph = graph (type = 'field', default_value = 0)
		self._value = 0
		Graphs._graphs.append(self)

	@property
	def value(self):
		return self._value

	@value.setter
	def value(self, tup):
		# сеттер для графика, принимает кортеж (значение, временной шаг)
		val = tup[0]
		tstep = tup[1]
		self._value = val
		self.graph[MODEL, tstep] = val

	@classmethod
	def export(cls, prefix):
		for item in cls._graphs:
			export (item.graph, name = prefix +'_' +item.name, units = item.units)


class Wells(metaclass = m):
	# класс хранит в себе все данные по скважинам из листа PVT и SKV
	_dic = {} # атрибут класса, хранит в себе все экземляры, может вызываться через __гетайтем

	def __init__(self, name = None, pusk_date = None, pvt = None, objects = None, ukpg = None, fond = None):
		self.name = name	#имя
		self.pusk_date = pusk_date	# дата запуска
		self.pvt = pvt # пвт таблица
		Wells._dic[name] = self
		self.is_active = None
		self.is_deleted = False
		self.objects = objects
		self.ukpg = ukpg
		self.fond = fond
		self.tovar_table = None
	def get_md(self, _wbp): 
		# возвращает мольную долю для расчета пластового газа
		return float(sum(kef*(_wbp**ind)for ind, kef in enumerate(self.pvt.md_suh_plast)))

	def get_plot(self, _wbp):
		# возвращает плотность конденсата для расчеты выхода конденсата из сухого газа
		return float(sum(kef*(_wbp**ind)for ind, kef in enumerate(self.pvt.plot_kond)))

	def get_md_sep(self, _wbp):
		# возвращает мольную долю для расчета газа сепарации
		return float(sum(kef*(_wbp**ind)for ind, kef in enumerate(self.pvt.md_sep_suh)))

	def get_kus(self, _wbp):
		# возвращает коэффициент усадки для расчета выхода нестабильного конденсата
		return float(sum(kef*(_wbp**ind)for ind, kef in enumerate(self.pvt.koef_usadki)))


	def get_multiplier(self, res_stab_cond = None):
	

		if len(self.tovar_table.mol_dol) == 2:
			mult_md = self.tovar_table.mol_dol[0]
			free_dick_md =  self.tovar_table.mol_dol[1]
			#print(res_stab_cond)
			mol_dol_sep_plast = mult_md*math.log(res_stab_cond) + free_dick_md
			
		else:
			mol_dol_sep_plast = sum([val*(res_stab_cond**ind) for ind, val in enumerate(self.tovar_table.mol_dol)])
			
		if len(self.tovar_table.ud_vyh) == 2:
			mult = self.tovar_table.ud_vyh[0]
			free_dick = self.tovar_table.ud_vyh[1]
			ud_vyh = mult*math.log(res_stab_cond) + free_dick
			
		else:
			ud_vyh = sum([val*(res_stab_cond**ind) for ind, val in enumerate(self.tovar_table.ud_vyh)])
			
		return ud_vyh, mol_dol_sep_plast

	@property
	def connections(self):
	# возвращает массив перфорация для скважины
		return get_well_by_name(self.name).connections	

	@property
	def tnav_obj(self):
	# возвращает объект встроенного класса в тнав
		return get_well_by_name (self.name)

	def is_opened(self, tstep):
		# возврашает статус скважины, True если открыта, False если закрыта
		l = self.tnav_obj.is_opened()
		if l[tstep]==1:
			return True
		elif l[tstep] == 0:
			return False

	@staticmethod
	def get_time_dif_indays(tstep, prev_tstep):
		# возвращает разницу между двумя датами в днях
		d0 = prev_tstep.to_datetime()
		d1 = tstep.to_datetime()
		delta = d1 - d0
		return delta.days
	
	def get_wetness(self, tstep, prev_tstep):
		global MODEL
		_wgpt = _cond_wetness= 0 
		con = self.connections
		total_gas_rate = wgpt[MODEL, self.tnav_obj, tstep] - wgpt[MODEL, self.tnav_obj, prev_tstep]
		if total_gas_rate < 0.1:
			return 0
			
		for c in con:
			_cbp = float(cbp[MODEL, c, tstep]) 
			func = Groups.Object.get_wetness_func(c.k)
			gas_rate_t = float(cgpt[MODEL, c, tstep] - cgpt[MODEL, c, prev_tstep])
			_cond_wetness += gas_rate_t*func(_cbp)
		return _cond_wetness
	
	def get_rate_of_object(self,object, tstep, prev_tstep):
		# возвращает суммарную добычу газа и нефти с объекта используя добычу по соединениям
		global MODEL
		con = self.connections
		_wgpt = _wopt = _woptf= _wwpt = _cond_wetness= 0 
		total_gas_rate = wgpt[MODEL, self.tnav_obj, tstep] - wgpt[MODEL, self.tnav_obj, prev_tstep]
		if total_gas_rate < 0.1:
			return 0, 0, 0, 0, 0
		for c in con:
			# если интервал перфорации лежит в пределах объекта разработки, то записываем значение в вектора
			if object.start <= c.k <= object.end:
				_cbp = float(cbp[MODEL, c, tstep])
				
				gas_rate_t = float(cgpt[MODEL, c, tstep] - cgpt[MODEL, c, prev_tstep])
				_cond_wetness += gas_rate_t*object.get_wetness(_cbp)
				_wgpt += gas_rate_t
				'''
				if object.name == 'I':
					#print(f'NEW METHOD CALLED FOR well = {self.name} object = {object.name}')
					try:
						oil_rate = gas_rate_t*interpolate(_cbp)
						_wopt += oil_rate
						#if self.name =='31801':
						#	print('cbp=', _cbp, 'int = ',  interpolate(_cbp), oil_rate, gas_rate_t)
					except TypeError:
						#print(_cbp, self.name, tstep.name)
						raise Exception
				else:
				'''
				_wopt += float(copt[MODEL, c, tstep] - copt[MODEL, c, prev_tstep])
				_woptf += float(coptf[MODEL, c, tstep] - coptf[MODEL, c, prev_tstep])
				_wwpt += float(cwpt[MODEL, c, tstep] - cwpt[MODEL, c, prev_tstep])
		#print(self.name, _cond_wetness)
		
		return float(_wgpt), float(_wopt), float(_woptf), float(_wwpt), float(_cond_wetness)

	@classmethod
	def get_gas(cls,index, tstep, prev_tstep, group, object):
		# возвращает все показатели для выгрузки
		total_dry_gas = total_plast_gas = total_oil = total_gas_sep = nestab_cond = cond_wetness= 0
		active_wells = 0
		deleted_wells = 0
		cum_wbp = cum_wbhp = cum_wthp = 0
		_wwt = 0
		water_rate = 0
		_dic = {}
		for well in group:
			# Принимаем, что скважина не работает на начало временного шага
			well.is_active = False
			#давление в барах
			_wbp = wbp[MODEL, well.tnav_obj, tstep]/10
			_wgpt = _wopt = _woptf = _wwpt = 0
			
			# Булева переменная, проверяет работает ли скважина на данный объект
			does_well_belong_to_object = object.name in well.objects
			
			if does_well_belong_to_object:
				_wwt += float(wwt[MODEL, well.tnav_obj, tstep])
				#print(tstep.name, well.name, wwt[MODEL, well.tnav_obj, tstep], )
			if object.name != 'all':
				# если конкретный объект разработки - показатели собираются по соединениям
					
				_wgpt, _wopt, _woptf, _wwpt, _cond_wetness = well.get_rate_of_object(object, tstep, prev_tstep)
				

				if abs (_wgpt) > 0.1:
				
					'''
					если есть добыча (или поглощение) за временной шаг, то скважина работает на данном временном шаге, 
					собираем накопленные показатели для группы, вместо wef используется время работы на временном шаге (вектор wwt)
					'''
					
					
					cum_wbp += float(_wbp)
					cum_wbhp += float(wbhp[MODEL, well.tnav_obj, tstep]/10)
					cum_wthp += float(wthp[MODEL, well.tnav_obj, tstep]/10)
				
				if float(wgpt[MODEL, well.tnav_obj, tstep] - wgpt[MODEL, well.tnav_obj, prev_tstep]) > 0.1 and does_well_belong_to_object:
					'''
					Если скважина что-то добыла за временной шаг неважно с какого объекта (добыча не по соединениям, 
					а с целой скважины, вектор wgpt), то скважина принимается активной. Если добыча = 0, то скважина неактивна
					'''
					well.is_active = True
				else:
					well.is_active = False
			else:
				#если объект - вся группа, то сумма показателей по целой скважине
				_wgpt = float(wgpt[MODEL, well.tnav_obj, tstep] - wgpt[MODEL, well.tnav_obj, prev_tstep])				
				_wopt = float(wopt[MODEL, well.tnav_obj, tstep] - wopt[MODEL, well.tnav_obj, prev_tstep])
				_woptf = float(woptf[MODEL, well.tnav_obj, tstep] - woptf[MODEL, well.tnav_obj, prev_tstep])
				_wwpt = float(wwpt[MODEL, well.tnav_obj, tstep] - wwpt[MODEL, well.tnav_obj, prev_tstep])		
				_cond_wetness = well.get_wetness(tstep, prev_tstep)
				if _wgpt > 0.0001:
					'''
					Если скважина имеет добыча за отчетном шаге, собираем показатели
					'''
					well.is_active	= True
					#_wwt += float(wwt[MODEL, well.tnav_obj, tstep])
					cum_wbp += float(_wbp)
					cum_wbhp += float(wbhp[MODEL, well.tnav_obj, tstep]/10)
					cum_wthp += float(wthp[MODEL, well.tnav_obj, tstep]/10)
				else: 
					well.is_active = False
			
			#сухой газ
			total_dry_gas += _wgpt
			#газ в пластовых условиях, md - мольная доля для перевода в пластовые условия
			md = well.get_md(_wbp)
			_plast_gas = _wgpt/md
			total_plast_gas += _plast_gas
			#конденсат, plot - плотность
			plot = well.get_plot(_wbp)
			total_oil += _wopt*plot
			cond_wetness += _cond_wetness
			#газ сепарации, md_sep - кэф для расчета
			#md_sep = well.get_md_sep(_wbp) #- deprecated
			#total_gas_sep += _wgpt*md_sep #- deprecated
			#нестабильный конденсат, ku - коэффиицент усадки
			#ku = well.get_kus(_wbp)#- deprecated
			#nestab_cond += _wopt*plot/ku  #- deprecated
			
			water_rate += _wwpt
			
			try:
				res_stab_cond = _wopt*plot*10**9/(_wgpt/md)/1000
				if res_stab_cond > 0 and _wopt > 0:
					res =  well.get_multiplier(res_stab_cond)
					
					gas_sep =res[1]*_wgpt/md
					total_gas_sep += gas_sep
					_nestab_cond = res[0]*gas_sep/1000000
					nestab_cond += _nestab_cond
					#print(well.name, res_stab_cond, res, _wopt, _wgpt)
			except ZeroDivisionError:
				res_stab_cond = 0
				gas_sep = 0
				_nestab_cond = 0
			
				pass
			if well.is_active:
				active_wells += 1
				
			'''
				Кусок кода для расчета выбытия скважин, он немного кривой, надо довести до ума.
				Работает следующим образом:
				1. Проверяется условие, НЕ выбыла ли скважина до этого И работает ли скважина на объект 
				2. Если 1ый пункт выполнен, то принимается допущение, что у скважины есть какая-то добыча 
				когда-то в будушем 
				3. Далее проверяется, условие: если накопленная добыча на последний временной шаг 
				равна накопленной добыче на текущий временной шаг (по факту используется трешхолд в 0,01), то у скважины нет отобора
				с пласта, и она может быть принята выбывшей 
				4. Переменная deleted_wells хранит количество выбывших скважин за текущий временной шаг
			'''
			
			if not well.is_deleted and does_well_belong_to_object:
				#q_flag = True
				#for  item in TIMESTEPS:
				if abs(float(wgpt[MODEL, well.tnav_obj, TIMESTEPS[-1]] - wgpt[MODEL, well.tnav_obj, tstep])) < 0.1:
					#print(well.name)
					#q_flag = False
					#break
				#if q_flag:
					#if not well.is_deleted:
					deleted_wells += 1
					#well_list.append(well.name)
					well.is_deleted = True
					well.is_active = False
			'''
					0: 'dry_gas',
					1: 'stab_cond',
					2: 'res_gas',
					3: 'gas_sep',
					4: 'nestab_cond',
					5: 'wbp',
					6: 'wbhp',
					7: 'wthp'
			'''
			
			if does_well_belong_to_object:
				kwargs = {
				'dry_gas': _wgpt,
				'stab_cond': _wopt*plot,
				'res_gas': _plast_gas,
				'gas_sep': gas_sep,
				'nestab_cond': _nestab_cond,
				'wbp': float(_wbp),
				'wbhp': float(wbhp[MODEL, well.tnav_obj, tstep]/10),
				'wthp': float(wthp[MODEL, well.tnav_obj, tstep]/10)
				}
				_dic[well.name] = Welldataholder (well.name, tstep.name, kwargs)
		try:
			# Средние показатели
			average_wbp = cum_wbp / active_wells
			average_wbhp = cum_wbhp / active_wells
			average_wthp = cum_wthp / active_wells
		except ZeroDivisionError as z:
			# Если нет действующих скважин
			average_wbp = 0
			average_wbhp = 0
			average_wthp = 0
			print(f'\tfor {tstep.name} active wells = {active_wells}')
		# возвращает показатели за текущий временной шаг в виде кортежа
		return (_wwt, # количество дней работы скважин	
			 active_wells, # действующий фонд
			 deleted_wells, # выбытие 
			 average_wbp,  # среднее давление в ПЗП
			 average_wbhp, # среднее забойное давление
			 average_wthp, # среднее устьевое давление 
			 total_dry_gas/(10**9),	 # добыча сухого газа в млрд куб м
			 total_plast_gas/(10**9), # добыча пластового газа в млрд куб м
			 total_oil/1000, # добыча конденсата в тыс т
			 total_gas_sep/(10**9), # добыча газа сепарации в млрд куб м
			 nestab_cond/1000, # добыча нестабильного конденсата в тыс т
			 water_rate,
			 cond_wetness/1000000,
			 _dic) 

	@classmethod
	def create_wells(cls):
		# Инициализация скважин из файлика well_table.txt
		well_table = open(DATAPATH + _FILENAME, 'r')
		lines = well_table.readlines()
		well_table.close()

		PVT_table.get_pvt_table()
		TovarProdTable.create_table()
		for line in lines:

			splitted_line =line.split() 
			name = splitted_line[0]
			fond = splitted_line[1]
			pusk_date = splitted_line[2] 
			pvt_num = int(splitted_line[4])
			ukpg = splitted_line[5]
			objects = ['all']
			objects.append(splitted_line[6])
			if len(splitted_line) ==8:
				objects.append(splitted_line[7])
			#print(name, objects)
			well = cls(name, pusk_date, PVT_table[pvt_num], objects, ukpg ,fond)
			well.tovar_table = TovarProdTable.get_table(ukpg, fond)
	@classmethod
	def clear_wells(cls):
		for well in cls._dic.values():
			well.is_active = False
			well.is_deleted = False


class TovarProdTable:
	_reg = {}
	def __init__(self, ukpg, fond):
		self.mol_dol = []
		self.ud_vyh = []
		self.ukpg = ukpg
		self.fond = fond
		TovarProdTable._reg[ukpg, fond] = self
	
	@classmethod
	def create_table(self):
		with open(DATAPATH + 'tovar_prod_table.txt', 'r') as f:
			lines = f.readlines()
		for line in lines:
			spl_line = re.split('\s|\t', line)
			ukpg = spl_line[1]
			fond = spl_line[2]
			vals = [float(item.replace('\n', '')) for item in filter(lambda x: x!= '', spl_line[3:])]
			try:
				obj = TovarProdTable._reg[ukpg, fond]
			except KeyError:
				obj = TovarProdTable(ukpg, fond)
			
			if 'MOL_DOL' in line:
				obj.mol_dol = vals
			else:
				obj.ud_vyh = vals
				
	@classmethod
	def get_table(cls, ukpg, fond):
		return cls._reg[ukpg, fond]
		
	def __repr__(self):
		return f'ukpg = {self.ukpg} fond = {self.fond} md = {self.mol_dol} udvyh = {self.ud_vyh}'				

				
###################################
class PVT_table(metaclass = m):
	_dic = {}
	'''
	Класс-контейнер, хранит в себе набор PVT-таблиц
	из файла pvt_table.txt. Каждый экземпляр класса - PVT-таблица
	'''
	def __init__(self, number = None, ukpg = None, object = None):
		self.number = number
		self.ukpg = ukpg
		self.object = object
		self.plot_kond = None
		self.md_suh_plast = None
		self.md_sep_suh = None
		self.koef_usadki = None
		PVT_table._dic[number] = self
	

	@classmethod
	def get_pvt_table(cls):
	#Функция парсит файл pvt_table.txt и создает экзмепляр класса пвт таблицы с данными
		for i in range(1,7):
			if i == 1:
				ukpg = '1B'
				object = 'I'
			elif i == 2:
				ukpg = '2B'
				object = 'I'	
			elif i == 3:
				ukpg = '3B'
				object = 'I'
			elif i == 4:
				ukpg = '1B'
				object = 'II'
			elif i == 5:
				ukpg = '2B'
				object = 'II'
			elif i == 6:
				ukpg = '3B'
				object = 'II'			
			table = PVT_table(i, ukpg, object)
			
		pvt_table = open(DATAPATH + 'pvt_table.txt', 'r')
		lines = pvt_table.readlines()
		pvt_table.close()
		for line in lines:
			splitted_line = line.split()
			number = int(splitted_line[1])
			type = splitted_line[0]
			kef_holder = np.empty(7)
			for i in range(0,7):
				try:
					kef_holder[i] = splitted_line[4+i]
				except IndexError:
					kef_holder[i] = 0
			if type == 'Plot_KOND':
				cls[number].plot_kond = kef_holder 
			elif type == 'MOL_DOL_SUH_PLAST':
				cls[number].md_suh_plast = kef_holder 
			elif type == 'MOL_DOL_SEP_SUH':
				cls[number].md_sep_suh = kef_holder 
			elif type == 'KOEFF_USADKI':
				cls[number].koef_usadki = kef_holder 
	

#creating well objects for each well

Wells.create_wells()	



#for well in Wells._dic.values():
#	print(well.name, well.ukpg, well.fond, well.get_multiplier(95.06))
'''
Создание групп по принадежности скважин
'''

#################################

all = Groups ('FIELD') #Месторождение

##################################

_1b_old = Groups('FIELD1')# 1B_old

#################################

_1b_new = Groups('FIELD1N') #1B_new

################################

_2b_old = Groups('FIELD2') #2B_old

#################################

_3b_old = Groups('FIELD3')#3B_old

#################################

_2b_new = Groups('FIELD2N')#2B_new

################################

_1b_new_2 = Groups('FIELD1NN') 

_2b_new_2 = Groups('FIELD2NN') 

Groups.get_groups()


ukpg_1 = _1b_old + _1b_new + _1b_new_2 #1B_all
ukpg_2 = _2b_old + _2b_new + _2b_new_2 
#_2b_all = _2b_old + _2b_new #2B_all



'''
Экземпляры класса Graphs, для удобной выгрузки и экспорта графиков
'''
plast_gas_rate = Graphs('Отбора пластового газа за период', "reservoir_rate")
plast_total = Graphs('Отбора пластового газа накопл', "reservoir_rate")
dry_gas_rate  = Graphs('Отбор сухого газа за период', 'gas_surface_rate')
dry_total = Graphs('Отбор сухого газа накопл', 'gas_surface_rate')
res_stab_cond = Graphs('Ресурсы стабильного конденсата')
oil_rate = Graphs('Отбор стабильного конденсата за период', "reservoir_rate")
oil_total = Graphs('Отбор стабильного конденсата накопл', "reservoir_rate")
gas_sep = Graphs('Газ сепарации', 'gas_surface_rate')
ud_nestab_yield = Graphs('Выход конденсата')
lic_wells = Graphs('Выбытие скважин')
active_wells = Graphs('Действующий фонд')
average_gas_rate = Graphs('Средний дебит газа', 'gas_surface_rate')
average_wbp = Graphs('Среднее пластовое давление', 'pressure')
average_wbhp = Graphs('Среднее забойное давление', 'pressure')
average_wthp = Graphs('Среднее устьевое давление', 'pressure')
nestab_cond = Graphs('Выход нестабильного конденсата')
water_rate =  Graphs('Отбор воды')
cond_wetness = Graphs('конденсационная вязкость')


def sort_dict(welldata):
	list_of_keys = sorted(welldata.keys())
	
	dic = {}
	for key in list_of_keys:
		dic[key] = welldata[key]
	return dic



def main(group, obj, output_welldata = False):
# главная функция, записывает все показатели в текстовый файл
	'''
	Удаление состояния скважин
	'''
	Wells.clear_wells()	
	global START_DATE
	
	'''
	group - экземпляр класса Gч объекта, 
	object - экземпляр вложенного класса Objects класса Groups
	obj - ключ
	'''
	
	try:	
		object = group[obj]
	except KeyError:
		raise ObjectNotFoundError(f'there is no object named {obj.name}')
	Path(DATAPATH + 'results').mkdir(parents=True, exist_ok = True)
	file = open(DATAPATH + 'results' + r'\{mname}_{name}_{object.name}.txt'.format(mname = MODEL.name, name=group.name, object = object), 'w')
	
	'''
	Если объект - это все объекты разработки, то хедеры будут отличаться.
	'''
	if object.name == 'all': #or object.name =='I' or object.name == 'II':
		file.write('date\t\
plast_rate\t\
plast_total\t\
dry_rate\t\
dry_total\t\
res_stab_cond\t\
condensate\t\
condensate_total\t\
gas_sep\t\
nestab_cond\t\
ud_vyhod_nestab_cond\t\
new_wells\t\
del_wells\t\
deistv_fond\t\
av_q\t\
av_wbp\t\
av_wbhp\t\
av_thp\t\
wef\t\
water_rate\t\
cond_wetness\n')
		try:
			ud_vyhod_nestab_cond = object.nestab_cond/object.gas_sep_rate
			res_stab_c = object.oil_rate/object.plast_rate
		except ZeroDivisionError:
			ud_vyhod_nestab_cond = 0
			res_stab_c = 0
			
		file.write(f'текущее сост\t\
{object.plast_rate:0.{PRECISION}f}\t\
{object.plast_total:0.{PRECISION}f}\t\
{object.dry_rate:0.{PRECISION}f}\t\
{object.dry_total:0.{PRECISION}f}\t\
{res_stab_c:0.{PRECISION}f}\t\
{object.oil_rate:0.{PRECISION}f}\t\
{object.oil_total:0.{PRECISION}f}\t\
{object.dry_total/object.res_gas:0.{PRECISION}f}\t\
{object.oil_total/object.res_oil:0.{PRECISION}f}\t\
{object.gas_sep_rate:0.{PRECISION}f}\t\
{object.nestab_cond:0.{PRECISION}f}\t\
{ud_vyhod_nestab_cond:0.{PRECISION}f}\n')

		'''
		В случае если объект не все месторождение
		'''
	else:
		file.write('date\t\
plast_rate\t\
plast_total\t\
dry_rate\t\
dry_total\t\
res_stab_cond\t\
condensate\t\
condensate_total\t\
gas_sep\t\
nestab_cond\t\
ud_vyhod_nestab_cond\t\
new_wells\t\
del_wells\t\
deistv_fond\t\
av_q\t\
av_wbp\t\
av_wbhp\t\
av_thp\t\
wef\t\
water_rate\t\
cond_wetness\n')


		try:
			ud_vyhod_nestab_cond = object.nestab_cond/object.gas_sep_rate
			res_stab_c = object.oil_rate/object.plast_rate
		except ZeroDivisionError:
			ud_vyhod_nestab_cond = 0
			res_stab_c = 0 
			print('No input data')
			
		file.write(f'текущее сост\t\
{object.plast_rate:0.{PRECISION}f}\t\
{object.plast_total:0.{PRECISION}f}\t\
{object.dry_rate:0.{PRECISION}f}\t\
{object.dry_total:0.{PRECISION}f}\t\
{res_stab_c:0.{PRECISION}f}\t\
{object.oil_rate:0.{PRECISION}f}\t\
{object.oil_total:0.{PRECISION}f}\t\
{object.gas_sep_rate:0.{PRECISION}f}\t\
{object.nestab_cond:0.{PRECISION}f}\t\
{ud_vyhod_nestab_cond:0.{PRECISION}f}\n')


	
	
	flag = False # флаг, если True, то будут показатели будут выгружаться, работает как флаг для timestep-ов
	
	wdata_holder = []
	for index, tstep in enumerate(TIMESTEPS):
		if tstep.name == START_DATE:
			flag =True
			plast_total.value = (object.plast_total, tstep)
			dry_total.value = (object.dry_total, tstep)
			oil_total.value = (object.oil_total, tstep)
		if flag:	
			
			prev_tstep = TIMESTEPS[index - 1] #предыдущий шаг для работы с накопленными показателями
			
			
			result = Wells.get_gas(index, tstep, prev_tstep, group, object)	#кортеж показателей
			wwt = result[0] #время работы
			active_wells.value = (result[1], tstep) #действующий фонд
			lic_wells.value = (result[2], tstep) # выбытие
			average_wbp.value = (result[3], tstep) #среднее давление в ПЗП
			average_wbhp.value =( result[4], tstep) # среднее забойной давление
			average_wthp.value = (result[5], tstep) # среднее устьевое давление
			dry_gas_rate.value = (result[6], tstep) # дебит сухого газа
			plast_gas_rate.value = (result[7], tstep) # дебит газа в пластовых условиях
			oil_rate.value = (result[8], tstep) # дебит конденсата
			gas_sep.value = (result[9], tstep) # дебит газа сепарации
			nestab_cond.value = (result[10], tstep) # дебит нестабильного конденсата
			water_rate.value = (result[11], tstep)
			cond_wetness.value = (result[12], tstep) #condensate wetness
			welldata = sort_dict(result[13])

			wdata_s = f'{tstep.name}\t'
			for item, value in welldata.items():
				wdata_s += value.output_data()
			wdata_holder.append(wdata_s)

			try:
				'''
				Следующие показатели рассчитываются от какой-то фактической точки из папки //groups 
				(метод get_group класса Groups). Если нет, то показатели будут ноль
				'''
				res_stab_cond.value = (oil_rate.value/plast_gas_rate.value, tstep) # стабильный конденсат
				ud_nestab_yield.value = (nestab_cond.value / gas_sep.value, tstep) # выход нестабильного конденсата
				average_gas_rate.value = (plast_gas_rate.value/wwt*1000000, tstep) # средний дебит газа
			except ZeroDivisionError:
				res_stab_cond.value = (0, tstep)
				ud_nestab_yield.value = (0, tstep)
				average_gas_rate.value = (0, tstep)

			plast_total.value = (plast_total.value + plast_gas_rate.value, tstep) # накопленный газ в пласт условиях
			dry_total.value = (dry_total.value + dry_gas_rate.value, tstep) # накопленный сухой газ
			oil_total.value = (oil_total.value	+ oil_rate.value, tstep) # накопленный конденсат
			gas_recovery = dry_total.value/object.res_gas # КИГ
			oil_recovery = oil_total.value/object.res_oil # КИК
			
			'''
			Если объект = all, то необходимо немного расширить данные для выгрузки
			'''
			if object.name == 'all':
				file.write(f'{tstep.name}\t\
{plast_gas_rate.value:0.{PRECISION}f}\t\
{plast_total.value:0.{PRECISION}f}\t\
{dry_gas_rate.value:0.{PRECISION}f}\t\
{dry_total.value:0.{PRECISION}f}\t\
{res_stab_cond.value:0.{PRECISION}f}\t\
{oil_rate.value:0.{PRECISION}f}\t\
{oil_total.value:0.{PRECISION}f}\t\
{gas_sep.value:0.{PRECISION}f}\t\
{nestab_cond.value:0.{PRECISION}f}\t\
{ud_nestab_yield.value:0.{PRECISION}f}\t\
0\t\
{lic_wells.value}\t\
{active_wells.value:0.0f}\t\
{average_gas_rate.value:0.{PRECISION}f}\t\
{average_wbp.value:0.{PRECISION}f}\t\
{average_wbhp.value:0.{PRECISION}f}\t\
{average_wthp.value:0.{PRECISION}f}\t\
{wwt:0.{PRECISION}f}\t\
{water_rate.value:0.{PRECISION}f}\t\
{cond_wetness.value:0.{PRECISION}f}\n')
			else:
				file.write(f'{tstep.name}\t\
{plast_gas_rate.value:0.{PRECISION}f}\t\
{plast_total.value:0.{PRECISION}f}\t\
{dry_gas_rate.value:0.{PRECISION}f}\t\
{dry_total.value:0.{PRECISION}f}\t\
{res_stab_cond.value:0.{PRECISION}f}\t\
{oil_rate.value:0.{PRECISION}f}\t\
{oil_total.value:0.{PRECISION}f}\t\
{gas_sep.value:0.{PRECISION}f}\t\
{nestab_cond.value:0.{PRECISION}f}\t\
{ud_nestab_yield.value:0.{PRECISION}f}\t\
0\t\
{lic_wells.value}\t\
{active_wells.value:0.0f}\t\
{average_gas_rate.value:0.{PRECISION}f}\t\
{average_wbp.value:0.{PRECISION}f}\t\
{average_wbhp.value:0.{PRECISION}f}\t\
{average_wthp.value:0.{PRECISION}f}\t\
{wwt}\t\
{water_rate.value:0.{PRECISION}f}\t\
{cond_wetness.value:0.{PRECISION}f}\n')
		
			print(f'tstep {tstep.name} done')
		#if tstep.name == '01.04.2021':
		#	break
	Graphs.export(group.name + '_' + object.name)
	header = Welldataholder.output_header(welldata)
	data = '\n'.join(wdata_holder)
	total = header + data
	
	with open(path.join(DATAPATH, 'results\\') + f'wells_{MODEL.name}.txt', 'w' ) as f:
		f.write(total)
	
# main(_1b_old, # Группа: all, _1b_old, _1b_new, _1b_all, _2b_old, _2b_new, _2b_all, _3b_old
#		'all' # Объект: 'I', 'II' - Объекты; 1-17 пласты
#		)

if _GROUP == 'all':
	_g = all
elif _GROUP == 'ukpg_1':
	_g = ukpg_1
elif _GROUP == '_1b_old':
	_g = _1b_old
elif _GROUP == '_1b_new':
	_g = _1b_new
elif _GROUP == '_1b_new_2':
	_g = _1b_new_2
elif _GROUP == 'ukpg_2':
	_g = ukpg_2
elif _GROUP == '_2b_old':
	_g = _2b_old
elif _GROUP == '_2b_new':
	_g = _2b_new
elif _GROUP == '_2b_new_2':
	_g = _2b_new_2
elif _GROUP == '_3b_old':
	_g = _3b_old


main(_g, _OBJECT)


#main(all, 'I')
#main(all, 'II')
#main(ukpg_1, 'all')
#main(_1b_old, 'all')
#main(_1b_new, 'all')
#main(_1b_new_2, 'all')
#main(ukpg_2, 'all')
#main(_2b_old, 'all')
#main(_2b_new, 'all')
#main(_2b_new_2, 'all')
#main(_3b_old, 'all')


