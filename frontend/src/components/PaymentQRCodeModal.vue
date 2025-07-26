<template>
  <div class="payment-modal-backdrop">
    <div class="payment-modal-content shadow-lg">
      <div class="payment-header">
        <h5 class="modal-title">{{ title }}</h5>
        <button type="button" class="btn-close" @click="$emit('close')"></button>
      </div>
      <div class="payment-body">
        <p>请扫描下方二维码完成支付</p>
        <div class="qr-code-container">
          <!-- A generic placeholder SVG QR Code -->
          <svg width="200" height="200" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <path fill="#000" d="M0 0h20v20H0z M25 0h20v20H25z M50 0h20v20H50z M75 0h20v20H75z M0 25h20v20H0z M25 25h5v5h-5z M35 25h5v5h-5z M45 25h5v5h-5z M55 25h5v5h-5z M65 25h5v5h-5z M75 25h20v20H75z M0 50h20v20H0z M25 50h5v5h-5z M35 50h5v5h-5z M45 50h5v5h-5z M55 50h5v5h-5z M65 50h5v5h-5z M75 50h20v20H75z M0 75h20v20H0z M25 75h20v20H25z M50 75h20v20H50z M75 75h20v20H75z"/>
          </svg>
        </div>
        <p class="amount">支付金额: <strong class="text-danger">¥{{ amount.toFixed(2) }}</strong></p>
      </div>
      <div class="payment-footer">
        <button class="btn btn-secondary" @click="$emit('close')">取消支付</button>
        <button class="btn btn-success" @click="$emit('payment-successful')">我已完成支付</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    paymentType: {
      type: String,
      required: true,
    },
    amount: {
      type: Number,
      required: true,
    },
  },
  emits: ['close', 'payment-successful'],
  computed: {
    title() {
      return this.paymentType === 'alipay' ? '使用支付宝支付' : '使用微信支付';
    },
  },
};
</script>

<style scoped>
.payment-modal-backdrop {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex; justify-content: center; align-items: center; z-index: 1050;
}
.payment-modal-content { 
  background: #f4eff6; border-radius: 12px; 
  max-width: 400px; width: 90%; text-align: center; 
  border: 1px solid rgba(0,0,0,0.1);
}
.payment-header { 
  display: flex; justify-content: space-between; align-items: center; 
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #d5bcde;
}
.payment-body {
  padding: 1.5rem;
}
.qr-code-container {
  margin: 1rem 0;
  padding: 1rem;
  background-color: #fff;
  border-radius: 8px;
  display: inline-block;
}
.amount { font-size: 1.2rem; margin-top: 1rem; }
.payment-footer { 
  display: flex; justify-content: flex-end; gap: 0.75rem; 
  padding: 1rem 1.5rem;
  border-top: 1px solid #d5bcde;
  background-color: #e8ddee;
}
</style>
