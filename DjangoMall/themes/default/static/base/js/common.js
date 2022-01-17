/**
 * 对源数据截取decimals位小数，不进行四舍五入
 * @param {*} num 源数据
 * @param {*} decimals 保留的小数位数
 * 参考地址：https://blog.csdn.net/qq_42127308/article/details/80388398
 */
var cutOutNum = (num, decimals = 2) => {
  if (isNaN(num) || (!num && num !== 0)) {
    return '-'
  }
 
  function toNonExponential (_num) {
    var m = _num.toExponential().match(/\d(?:\.(\d*))?e([+-]\d+)/)
    return _num.toFixed(Math.max(0, (m[1] || '').length - m[2]))
  }
 
  // 为了兼容科学计数法的数字
  num = toNonExponential(num)
  // 获取小数点的位置 + 1（不存在小数点的indexOf值为-1）
  const pointIndex = String(num).indexOf('.') + 1
  // 获取小数点后的个数(需要保证有小数位)
  const pointCount = pointIndex ? String(num).length - pointIndex : 0
 
  // 补零函数
  function zeroFill (zeroNum, num) {
    for (let index = 0; index < zeroNum; index++) {
      num = `${num}0`
    }
    return num
  }
 
  // 源数据为"整数"或者小数点后面小于decimals位的作补零处理
  if (pointIndex === 0 || pointCount <= decimals) {
    let tempNumA = num
    // 区分"整数"和"小数"的补零
    if (pointIndex === 0) {
      tempNumA = `${tempNumA}.`
      tempNumA = zeroFill(decimals - pointCount, tempNumA)
    } else {
      tempNumA = zeroFill(decimals - pointCount, tempNumA)
    }
    return String(tempNumA)
  }
 
  // 截取当前数据到小数点后decimals位
  const Int = String(num).split('.')[0]
  const Decimal = String(num).split('.')[1].substring(0, decimals)
  const tempNumB = `${Int}.${Decimal}`
 
  // 需求：数据为0时，需要显示为0，而不是0.00...
  return Number(tempNumB) === 0 ? 0 : tempNumB
}