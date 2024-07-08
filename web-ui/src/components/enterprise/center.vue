<template>
	<!-- 功能栏 -->
	<el-row style="width: 100%;margin-top: 10px;margin-bottom: 20px;">
		<el-col :span="2">
			<el-button type="primary" @click="handleAdd">发布职位</el-button>
		</el-col>
		<el-col :span="10">
			<el-input placeholder="请输入搜索关键词" v-model="key" clearable></el-input>
		</el-col>
		<el-col :span="4">
			<el-button type="primary" @click="search">
				搜索
			</el-button>
		</el-col>
	</el-row>
	<!-- 职位列表 -->
	<el-table :data="tableData" style="width: 100%;margin-top: 10px;">
		<el-table-column label="职位名" prop="name" width="180">
		</el-table-column>
		<el-table-column label="职位类型" prop="worktype" width="180">
		</el-table-column>
		<el-table-column label="工作地点" prop="workcity" width="180">
		</el-table-column>
		<el-table-column label="薪资" prop="salary60" width="180">
		</el-table-column>
		<el-table-column label="学历要求" prop="education" width="180">
		</el-table-column>
		<el-table-column label="操作">
			<template #default="scope">
				<el-button size="small" type="primary">
					精准推荐
				</el-button>
				<el-button size="small" @click="handleEdit(scope.$index, scope.row)">
					编辑
				</el-button>
				<el-button size="small" type="danger" @click="handleDelete(scope.$index, scope.row)">
					删除
				</el-button>
			</template>
		</el-table-column>
	</el-table>
	<!-- 新增和编辑对话框 -->
	<el-dialog v-model="dialogVisible" :title="type" width="450px">
		<el-form :model="form">
			<el-form-item label="职位名">
				<el-input v-model="form.name" />
			</el-form-item>
			<el-form-item label="职位类型">
				<el-input v-model="form.worktype" />
			</el-form-item>
			<el-form-item label="工作地点">
				<el-input v-model="form.workcity" />
			</el-form-item>
			<el-form-item label="薪资">
				<el-input v-model="form.salary60" />
			</el-form-item>
			<el-form-item label="学历要求">
				<el-input v-model="form.education" />
			</el-form-item>
		</el-form>
		<template #footer>
			<div class="dialog-footer">
				<el-button @click="dialogVisible = false">取消</el-button>
				<el-button type="primary" @click="submit">
					确认
				</el-button>
			</div>
		</template>
	</el-dialog>
</template>

<script>
	export default {
		data() {
			return {
				//表格数据
				tableData: [],
				//新增和编辑数据
				form: {},
				//新增or编辑
				type: "新增",
				//控制对话框显示与否
				dialogVisible: false,
				//搜索关键词
				key: "",
			}
		},
		created() {
			this.getList();
		},
		methods: {
			//获取列表信息
			getList() {
				this.$http.get(this.$api.companyJobs, {
					headers: {
						'Content-Type': 'application/json',
					}
				}).then(response => {
					this.tableData = response.data.data;
				})
			},
			//点击编辑按钮
			handleEdit(index, row) {
				this.form = row;
				this.type = "编辑";
				this.dialogVisible = true;
			},
			//点击新增按钮
			handleAdd() {
				this.form = {};
				this.type = "新增";
				this.dialogVisible = true;
			},
			//点击删除按钮
			handleDelete(index, row) {
				this.$http.post(this.$api.removeJob, {
					'id': row.id,
				}).then(response => {
					ElMessage({
							message: '删除成功',
							type: 'success',
						}),
						//重新获取数据
						this.getList();
				})
			},
			//确认新增或编辑
			submit() {
				this.dialogVisible = false;
				if (this.type == "新增") {
					this.form.job_id = 1;
					this.form.number = 1;
					this.$http.post(this.$api.addJob,
						this.form
					).then(response => {
						ElMessage({
								message: '新增成功',
								type: 'success',
							}),
							//重新获取数据
							this.getList();
					})
				} else {
					this.$http.post(this.$api.editJob,
						this.form
					).then(response => {
						ElMessage({
								message: '编辑成功',
								type: 'success',
							}),
							//重新获取数据
							this.getList();
					})
				}
			},
			//搜索职位
			search() {
				if (this.key == '') return;
				this.$http.post(this.$api.searchJob, {
					'key': this.key,
				}).then(response => {
					this.tableData = response.data.data;
					this.key = "";
				});
			}
		}
	}
</script>

<style scoped>

</style>