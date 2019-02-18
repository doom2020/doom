from django.db import models

# Create your models here.
USER_STATUS = (
    (1, "有效"),
    (0, "无效"),
)
GOODS_STATUS = (
    (1, "上架"),
    (0, "下架"),
)
ORDER_STATUS = (
    (1, "已提交"),
    (2, "正在处理"),
    (3, "已取消"),
    (4, "已完成"),
)
#用户表
class UserInfo(models.Model):
    uname = models.CharField(max_length=50, verbose_name="用户昵称")
    upwd = models.CharField(max_length=60, verbose_name="用户密码")
    uphone = models.CharField(max_length=60, verbose_name="用户手机")
    uemail = models.EmailField(max_length=60, null=True, verbose_name="用户邮箱")
    upicture = models.ImageField(null=True, upload_to="static/image/user", verbose_name="用户头像")
    is_vaild = models.BooleanField(choices=USER_STATUS, default=1, verbose_name="有效用户")
    def __str__(self):
        return self.uname
    class Meta:
        db_table = 'userinfo'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
        ordering = ['id']

#地址表
class Address(models.Model):
    take_name = models.CharField(max_length=50, verbose_name="取件人")
    take_phone = models.CharField(max_length=100, verbose_name="取件人电话")
    address_name = models.CharField(max_length=200, verbose_name="收货地址")
    userinfo = models.ForeignKey(UserInfo, on_delete=True, null=True, verbose_name="买主")

    def __str__(self):
        return self.address_name
    class Meta:
        db_table = "address"
        verbose_name = "收件人信息"
        verbose_name_plural = verbose_name
        ordering = ['id']

#购物车表
class ShoppingCar(models.Model):
    userinfo = models.OneToOneField(UserInfo, on_delete=True, verbose_name="购物车主人", null=True)

    def __str__(self):
        return self.userinfo.uname
    class Meta:
        db_table = "shoppingcar"
        verbose_name = "购物车信息"
        verbose_name_plural = verbose_name

#订单表
class Order(models.Model):
    sum_money = models.DecimalField(verbose_name="订单总额", max_digits=10, decimal_places=2)
    userinfo = models.ForeignKey(UserInfo, on_delete=True, verbose_name="下订单用户", null=True)
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS, default=1, verbose_name="订单状态")

    def __str__(self):
        return self.userinfo.uname
    class Meta:
        db_table = "order"
        verbose_name = "订单信息"
        verbose_name_plural = verbose_name
        ordering = ["sum_money"]

#商品类型表
class GoodsType(models.Model):
    gtype_name = models.CharField(max_length=50, verbose_name="商品类型名称")
    def __str__(self):
        return self.gtype_name
    class Meta:
        db_table = "goodstype"
        verbose_name = "商品类型"
        verbose_name_plural = verbose_name
        ordering = ["gtype_name"]
#商品表
class Goods(models.Model):
    gname = models.CharField(max_length=50, verbose_name="商品名称")
    gprice = models.DecimalField(verbose_name="商品价格", max_digits=7, decimal_places=2)
    gpicture = models.ImageField(verbose_name="商品图片", upload_to="static/image/goods")
    g_vaild = models.BooleanField(verbose_name="是否上架", choices=GOODS_STATUS, default=1)
    shopping_car = models.ForeignKey(ShoppingCar, on_delete=True, null=True, verbose_name="商品的购物车")
    g_type = models.ForeignKey(GoodsType, on_delete=True, null=True, verbose_name="商品类型")
    def __str__(self):
        return self.gname
    class Meta:
        db_table = "goods"
        verbose_name = "商品信息"
        verbose_name_plural = verbose_name
        ordering = ["gprice"]

